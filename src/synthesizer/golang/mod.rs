use crate::ir::conditions::ConditionIr;
use crate::ir::constructor::ConstructorParameter;
use crate::ir::importer::ImportInstruction;
use crate::ir::mappings::OutputType;
use crate::ir::reference::{Origin, PseudoParameter, Reference};
use crate::ir::resources::{find_references, ResourceIr};
use crate::ir::CloudformationProgramIr;
use crate::parser::lookup_table::MappingInnerValue;
use crate::specification::{CfnType, Structure};
use std::borrow::Cow;
use std::io;
use voca_rs::case::{camel_case, pascal_case, snake_case};

use super::output::CodeSink;
use super::Synthesizer;

pub struct Golang {
    package_name: String,
}

impl Golang {
    pub fn new(package_name: impl Into<String>) -> Self {
        Self {
            package_name: package_name.into(),
        }
    }
}

impl Default for Golang {
    fn default() -> Self {
        Self::new("main")
    }
}

impl Synthesizer for Golang {
    fn synthesize(&self, ir: CloudformationProgramIr, into: &mut dyn io::Write) -> io::Result<()> {
        let mut output = CodeSink::golang(into);

        output.write_line(&format!("package {}", self.package_name))?;
        output.blank_line()?;

        output.write_line("import (")?;
        let imports = &mut output.indented();
        imports.write_line("\"fmt\"")?;
        imports.blank_line()?;
        for import in ir.imports {
            imports.write_line(&import.to_golang())?;
        }
        // The usual imports of constructs library & jsii runtime
        imports.write_line("\"github.com/aws/constructs-go/constructs/v10\"")?;
        imports.write_line("\"github.com/aws/jsii-runtime-go\"")?;
        output.write_line(")")?;
        output.blank_line()?;

        output.write_line("type NoctStackProps struct {")?;
        let props = &mut output.indented();
        props.write_line("cdk.StackProps")?; // Extends cdk.StackProps
        for param in &ir.constructor.inputs {
            if let Some(description) = &param.description {
                props.write_with_prefix("/// ", description)?;
            }
            props.write_line(&param.to_golang_field())?;
        }
        output.write_line("}")?;
        output.blank_line()?;

        if let Some(description) = &ir.description {
            output.write_with_prefix("/// ", description)?;
        }
        output.write_line("type NoctStack struct {")?;
        let class = &mut output.indented();
        class.write_line("cdk.Stack")?;
        for output in &ir.outputs {
            if let Some(description) = &output.description {
                class.write_with_prefix("/// ", description)?;
            }
            class.write_line(&format!(
                "{name} interface{{}}",
                name = golang_identifier(&output.name, IdentifierKind::Exported)
            ))?; // TODO: Type?
        }
        output.write_line("}")?;
        output.blank_line()?;

        output.write_line(
            "func NewNoctStack(scope constructs.Construct, id string, props NoctStackProps) *NoctStack {",
        )?;
        let ctor = &mut output.indented();

        for mapping in &ir.mappings {
            let leaf_type = match mapping.output_type() {
                OutputType::Complex => "interface{}",
                OutputType::Consistent(inner) => match inner {
                    MappingInnerValue::Bool(_) => "*bool",
                    MappingInnerValue::Float(_) | MappingInnerValue::Number(_) => "*float64",
                    MappingInnerValue::String(_) => "*string",
                    MappingInnerValue::List(_) => "[]*string",
                },
            };
            ctor.write_line(&format!(
                "{} := map[*string]map[*string]{leaf_type}{{",
                golang_identifier(&mapping.name, IdentifierKind::Unexported)
            ))?;
            let map = &mut ctor.indented();
            for (key, inner) in &mapping.map {
                map.write_line(&format!("jsii.String({key:?}): map[*string]{leaf_type}{{"))?;
                let inner_map = &mut map.indented();
                for (key, value) in inner {
                    inner_map.write(&format!("jsii.String({key:?}): "))?;
                    match value {
                        MappingInnerValue::Bool(bool) => {
                            inner_map.write_raw(&format!("jsii.Bool({bool})"), false)?
                        }
                        MappingInnerValue::Number(num) => {
                            inner_map.write_raw(&format!("jsii.Number({num})"), false)?
                        }
                        MappingInnerValue::Float(num) => {
                            inner_map.write_raw(&format!("jsii.Number({num})"), false)?
                        }
                        MappingInnerValue::String(str) => {
                            inner_map.write_raw(&format!("jsii.String({str:?})"), false)?
                        }
                        MappingInnerValue::List(items) => {
                            inner_map.write_raw_line("[]*string{", false)?;
                            let list = &mut inner_map.indented();
                            for item in items {
                                list.write_line(&format!("jsii.String({item:?}),"))?;
                            }
                            inner_map.write("}")?;
                        }
                    }
                    inner_map.write_raw_line(",", false)?;
                }
                map.write_line("},")?;
            }
            ctor.write_line("}")?;
            ctor.blank_line()?;
        }

        ctor.write_line("stack := cdk.NewStack(scope, &id, &props.StackProps)")?;
        ctor.blank_line()?;

        for condition in &ir.conditions {
            ctor.write(&format!(
                "{name} := ",
                name = golang_identifier(&condition.name, IdentifierKind::Unexported)
            ))?;
            condition.value.emit_golang(ctor, false, None)?;
            ctor.blank_line()?;
            ctor.blank_line()?;
        }

        for resource in &ir.resources {
            let ns =
                golang_identifier(resource.resource_type.service(), IdentifierKind::ModuleName);
            let class = resource.resource_type.type_name();

            let prefix = if ir.resources.iter().any(|other| {
                other.name != resource.name && other.references.contains(&resource.name)
            }) || ir
                .outputs
                .iter()
                .any(|output| find_references(&output.value).contains(&resource.name))
            {
                format!(
                    "{varname} := ",
                    varname = golang_identifier(&resource.name, IdentifierKind::Unexported)
                )
            } else {
                "".into()
            };
            ctor.write_line(&format!("{prefix}{ns}.NewCfn{class}("))?;
            let params = &mut ctor.indented();
            params.write_line("stack,")?;
            params.write_line(&format!("jsii.String({:?}),", resource.name))?;
            params.write_line(&format!("&{ns}.Cfn{class}Props{{"))?;
            let props = &mut params.indented();
            for (name, value) in &resource.properties {
                props.write(&format!(
                    "{}: ",
                    golang_identifier(name, IdentifierKind::Exported)
                ))?;
                value.emit_golang(props, false, None)?;
                props.write_raw_line(",", false)?;
            }
            params.write_line("},")?;
            ctor.write_line(")")?;
            ctor.blank_line()?;
        }
        ctor.blank_line()?;

        ctor.write_line("return &NoctStack{")?;
        let fields = &mut ctor.indented();
        fields.write_line("Stack: stack,")?;
        for output in &ir.outputs {
            fields.write(&format!(
                "{name}: ",
                name = golang_identifier(&output.name, IdentifierKind::Exported)
            ))?;
            output.value.emit_golang(fields, false, None)?;
            fields.write_raw_line(",", false)?;
        }
        ctor.write_line("}")?;
        output.write_line("}")?;

        Ok(())
    }
}

impl ImportInstruction {
    fn to_golang(&self) -> String {
        let mut parts: Vec<Cow<str>> = vec![match self.path[0].as_str() {
            "aws-cdk-lib" => "github.com/aws/aws-cdk-go/awscdk/v2".into(),
            other => other.into(),
        }];
        parts.extend(self.path[1..].iter().map(|item| {
            item.chars()
                .filter(|ch| ch.is_alphanumeric())
                .collect::<String>()
                .into()
        }));

        format!(
            "{name} {module:?}",
            name = self.name,
            module = parts.join("/")
        )
    }
}

impl ConstructorParameter {
    fn to_golang_field(&self) -> String {
        format!(
            "{name} {type}",
            name = golang_identifier(&self.name, IdentifierKind::Exported),
            r#type = match self.constructor_type.as_ref() {
                "String" => "*string",
                other => unimplemented!("parameter type: {other}"),
            }
        )
    }
}

trait GolangEmitter {
    fn emit_golang(
        &self,
        output: &mut CodeSink,
        indent_lead: bool,
        trailer: Option<&str>,
    ) -> io::Result<()>;
}

impl GolangEmitter for ConditionIr {
    fn emit_golang(
        &self,
        output: &mut CodeSink,
        indent_lead: bool,
        trailer: Option<&str>,
    ) -> io::Result<()> {
        match self {
            Self::Equals(lhs, rhs) => {
                lhs.emit_golang(output, indent_lead, None)?;
                output.write_raw(" == ", false)?;
                rhs.emit_golang(output, false, None)?
            }
            Self::Ref(reference) => reference.emit_golang(output, indent_lead, None)?,
            Self::Str(str) => output.write_raw(&format!("jsii.String({str:?})"), indent_lead)?,
            other => output.write_raw(&format!("nil /* {other:?} */"), indent_lead)?,
        }
        if let Some(trailer) = trailer {
            output.write_raw_line(trailer, false)
        } else {
            Ok(())
        }
    }
}

impl GolangEmitter for ResourceIr {
    fn emit_golang(
        &self,
        output: &mut CodeSink,
        indent_lead: bool,
        trailer: Option<&str>,
    ) -> io::Result<()> {
        match self {
            // Canonical nil
            Self::Null => output.write_raw("nil", indent_lead)?,

            // Literal values
            Self::Bool(bool) => output.write_raw(&format!("jsii.Bool({bool})"), indent_lead)?,
            Self::Double(double) => {
                output.write_raw(&format!("jsii.Number({double})"), indent_lead)?;
            }
            Self::Number(number) => {
                output.write_raw(&format!("jsii.Number({number})"), indent_lead)?;
            }
            Self::String(text) => {
                output.write_raw(&format!("jsii.String({text:?})"), indent_lead)?;
            }

            // Composites
            Self::Array(structure, array) => {
                let value_type: Cow<str> = match structure {
                    Structure::Composite(name) => match *name {
                        "Tag" => "*cdk.CfnTag".into(),
                        name => todo!("Composite Array of {name}"),
                    },
                    Structure::Simple(simple) => match simple {
                        CfnType::Boolean => "*bool".into(),
                        CfnType::Double | CfnType::Integer | CfnType::Long => "*float64".into(),
                        CfnType::Json => "interface{}".into(),
                        CfnType::String => "*string".into(),
                        CfnType::Timestamp => "time.Date".into(),
                    },
                };

                output.write_raw_line(&format!("&[]{value_type}{{"), indent_lead)?;
                let items = &mut output.indented();
                for item in array {
                    item.emit_golang(items, true, None)?;
                    items.write_raw_line(",", false)?;
                }
                output.write_raw("}", true)?;
            }
            Self::Object(structure, properties) => {
                match structure {
                    Structure::Composite(name) => match *name {
                        "Tag" => output.write_raw_line("{", indent_lead)?,
                        name => todo!("Composite Object of {name}"),
                    },
                    Structure::Simple(_) => unreachable!(),
                }
                let props = &mut output.indented();
                for (name, val) in properties {
                    props.write_raw(
                        &format!(
                            "{name}: ",
                            name = golang_identifier(name, IdentifierKind::Exported)
                        ),
                        true,
                    )?;
                    val.emit_golang(props, false, Some(","))?;
                }
                output.write_raw("}", true)?;
            }

            // Intrinsic functions
            Self::Base64(value) => {
                output.write_raw("cdk.Fn_Base64(", indent_lead)?;
                value.emit_golang(output, false, None)?;
                output.write_raw(")", false)?;
            }
            Self::Cidr(cidr_block, count, mask) => {
                output.write_raw("cdk.Fn_Cidr(", indent_lead)?;
                cidr_block.emit_golang(output, false, None)?;
                output.write_raw(", ", false)?;
                count.emit_golang(output, false, None)?;
                output.write_raw(", ", false)?;
                // TODO: This should be a string for some reason...
                mask.emit_golang(output, false, None)?;
                output.write_raw(")", false)?;
            }
            Self::GetAZs(region) => {
                output.write_raw("cdk.Fn_GetAzs(", indent_lead)?;
                region.emit_golang(output, false, None)?;
                output.write_raw(")", false)?;
            }
            Self::If(cond, when_true, when_false) => {
                // TODO: This needs to return the appropriate value type...
                output.write_raw_line("func() interface{} {", indent_lead)?;
                let body = &mut output.indented();
                body.write_line(&format!(
                    "if {cond} {{",
                    cond = golang_identifier(cond, IdentifierKind::Unexported)
                ))?;
                let case = &mut body.indented();
                case.write_raw("return ", true)?;
                when_true.emit_golang(case, false, Some(""))?;
                body.write_line("} else {")?;
                let case = &mut body.indented();
                case.write_raw("return ", true)?;
                when_false.emit_golang(case, false, Some(""))?;
                body.write_line("}")?;
                output.write("}()")?;
            }
            Self::ImportValue(import) => output.write_raw(
                &format!("cdk.Fn_ImportValue(jsii.String({import:?}))"),
                indent_lead,
            )?,
            Self::Join(sep, list) => {
                output.write_raw_line(
                    &format!("cdk.Fn_Join(jsii.String({sep:?}), &[]*string{{"),
                    indent_lead,
                )?;
                let items = &mut output.indented();
                for item in list {
                    item.emit_golang(items, true, Some(","))?;
                }
                output.write_raw("})", true)?;
            }
            Self::Map(table, tlk, slk) => {
                output.write_raw(
                    &format!(
                        "{table}[",
                        table = golang_identifier(table, IdentifierKind::Unexported)
                    ),
                    indent_lead,
                )?;
                tlk.emit_golang(output, false, None)?;
                output.write_raw("][", false)?;
                slk.emit_golang(output, false, None)?;
                output.write_raw("]", false)?;
            }
            Self::Select(idx, list) => match list.as_ref() {
                ResourceIr::Array(_, items) => {
                    items[*idx].emit_golang(output, indent_lead, None)?;
                }
                list => {
                    output
                        .write_raw(&format!("cdk.Fn_Select(jsii.Number({idx}), "), indent_lead)?;
                    list.emit_golang(output, false, None)?;
                    output.write_raw(")", false)?;
                }
            },
            Self::Sub(parts) => {
                let pattern = parts
                    .iter()
                    .map(|part| match part {
                        ResourceIr::Bool(val) => val.to_string(),
                        ResourceIr::Double(val) => val.to_string(),
                        ResourceIr::Number(val) => val.to_string(),
                        ResourceIr::String(val) => val.clone(),
                        _ => "%v".into(),
                    })
                    .collect::<String>();
                output.write_raw(&format!("jsii.String(fmt.Sprintf({pattern:?}"), indent_lead)?;
                for part in parts {
                    match part {
                        ResourceIr::Bool(_)
                        | ResourceIr::Double(_)
                        | ResourceIr::Number(_)
                        | ResourceIr::String(_) => {}
                        part => {
                            output.write_raw(", ", false)?;
                            part.emit_golang(output, false, None)?;
                        }
                    }
                }
                output.write_raw("))", false)?;
            }

            // References
            Self::Ref(reference) => reference.emit_golang(output, indent_lead, None)?,

            // TODO: Drop this
            other => output.write_raw(&format!("nil /* {other:?} */"), indent_lead)?,
        }

        if let Some(trailer) = trailer {
            output.write_raw_line(trailer, false)
        } else {
            Ok(())
        }
    }
}

impl GolangEmitter for Reference {
    fn emit_golang(
        &self,
        output: &mut CodeSink,
        indent_lead: bool,
        trailer: Option<&str>,
    ) -> io::Result<()> {
        match &self.origin {
            Origin::Condition => todo!(),
            Origin::GetAttribute {
                attribute,
                conditional,
            } => output.write_raw(
                &format!(
                    "{name}.Attr{attribute}()",
                    name = golang_identifier(&self.name, IdentifierKind::Unexported),
                    attribute = golang_identifier(attribute, IdentifierKind::Exported),
                ),
                indent_lead,
            )?,
            Origin::LogicalId { conditional } => output.write_raw(
                &format!(
                    "{name}.Ref()",
                    name = golang_identifier(&self.name, IdentifierKind::Unexported)
                ),
                indent_lead,
            )?,
            Origin::Parameter => output.write_raw(
                &format!(
                    "props.{name}",
                    name = golang_identifier(&self.name, IdentifierKind::Exported)
                ),
                indent_lead,
            )?,
            Origin::PseudoParameter(pseudo) => {
                let pseudo = match pseudo {
                    PseudoParameter::AccountId => "Account",
                    PseudoParameter::Partition => "Partition",
                    PseudoParameter::Region => "Region",
                    PseudoParameter::StackId => "StackId",
                    PseudoParameter::StackName => "StackName",
                    PseudoParameter::URLSuffix => "UrlSuffix",
                    PseudoParameter::NotificationArns => "NotificationArns",
                };
                output.write_raw(&format!("stack.{pseudo}()"), indent_lead)?;
            }
        }

        if let Some(trailer) = trailer {
            output.write_raw_line(trailer, false)
        } else {
            Ok(())
        }
    }
}

#[derive(Clone, Copy)]
enum IdentifierKind {
    Exported,
    Unexported,
    ModuleName,
}

/// Computes a go identifier name that is a suitable representation of the given
/// name.
fn golang_identifier(text: &str, kind: IdentifierKind) -> String {
    match kind {
        IdentifierKind::Exported => pascal_case(text),
        IdentifierKind::ModuleName => snake_case(text),
        IdentifierKind::Unexported => camel_case(text),
    }
}
