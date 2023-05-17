#![allow(unused_variables)]

use crate::ir::conditions::ConditionIr;
use crate::ir::constructor::ConstructorParameter;
use crate::ir::importer::ImportInstruction;
use crate::ir::mappings::OutputType;
use crate::ir::reference::{Origin, PseudoParameter, Reference};
use crate::ir::resources::{find_references, ResourceInstruction, ResourceIr};
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
        {
            let mut insert_blank = if ir.requires_fmt() {
                imports.write_line("\"fmt\"")?;
                true
            } else {
                false
            };
            if ir.requires_time() {
                imports.write_line("\"time\"")?;
                insert_blank = true;
            }
            if insert_blank {
                imports.blank_line()?;
            }
        }

        for import in &ir.imports {
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
                "{name} interface{{}} // TODO: fix to appropriate type",
                name = golang_identifier(&output.name, IdentifierKind::Exported)
            ))?
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

            let used = ir.uses_map_table(&mapping.name);
            if !used {
                // Go is merciless about dead stores... so we comment out unused maps...
                ctor.write_line("/*")?;
            }
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
            if !used {
                ctor.write_line("*/")?;
            }
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

        for output in &ir.outputs {
            if let Some(export) = &output.export {
                ctor.write_line(&format!(
                    "cdk.NewCfnOutput(stack, jsii.String({name:?}), &cdk.CfnOutputProps{{",
                    name = output.name
                ))?;
                let props = &mut ctor.indented();
                if let Some(description) = &output.description {
                    props.write_line(&format!("Description: jsii.String({description:?}),"))?;
                }
                props.write("ExportName: ")?;
                export.emit_golang(props, false, Some(","))?;
                props.write("Value: ")?;
                output.value.emit_golang(props, false, Some(","))?;
                ctor.write_line("})")?;
                ctor.blank_line()?;
            }
        }

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

trait Inspectable {
    /// Whether the rendered code for this entity requires importing "fmt"
    fn requires_fmt(&self) -> bool;
    /// Whether the rendered code for this entity requires importing "time"
    fn requires_time(&self) -> bool;

    /// Whether the rendered code for this entity uses the named mapping table.
    fn uses_map_table(&self, name: &str) -> bool;
}

impl Inspectable for CloudformationProgramIr {
    fn requires_fmt(&self) -> bool {
        self.resources.iter().any(Inspectable::requires_fmt)
            || self.outputs.iter().any(|out| out.value.requires_fmt())
    }

    fn requires_time(&self) -> bool {
        self.resources.iter().any(Inspectable::requires_time)
            || self.outputs.iter().any(|out| out.value.requires_time())
    }

    fn uses_map_table(&self, name: &str) -> bool {
        self.conditions
            .iter()
            .any(|cond| cond.value.uses_map_table(name))
            || self.resources.iter().any(|res| res.uses_map_table(name))
            || self
                .outputs
                .iter()
                .any(|out| out.value.uses_map_table(name))
    }
}

impl Inspectable for ConditionIr {
    #[cfg_attr(coverage_nightly, no_coverage)]
    #[inline]
    fn requires_fmt(&self) -> bool {
        false
    }

    #[cfg_attr(coverage_nightly, no_coverage)]
    #[inline]
    fn requires_time(&self) -> bool {
        false
    }

    fn uses_map_table(&self, name: &str) -> bool {
        match self {
            ConditionIr::Equals(lhs, rhs) => lhs.uses_map_table(name) || rhs.uses_map_table(name),
            ConditionIr::Not(cond) => cond.uses_map_table(name),
            ConditionIr::And(list) | ConditionIr::Or(list) => {
                list.iter().any(|cond| cond.uses_map_table(name))
            }
            ConditionIr::Map(map_name, _, _) => map_name == name,
            ConditionIr::Str(_) | ConditionIr::Ref(_) => false,
        }
    }
}

impl Inspectable for ResourceInstruction {
    fn requires_fmt(&self) -> bool {
        self.properties.values().any(Inspectable::requires_fmt)
            || self
                .metadata
                .as_ref()
                .map(Inspectable::requires_fmt)
                .unwrap_or(false)
            || self
                .update_policy
                .as_ref()
                .map(Inspectable::requires_fmt)
                .unwrap_or(false)
    }

    fn requires_time(&self) -> bool {
        self.properties.values().any(Inspectable::requires_time)
            || self
                .metadata
                .as_ref()
                .map(Inspectable::requires_time)
                .unwrap_or(false)
            || self
                .update_policy
                .as_ref()
                .map(Inspectable::requires_time)
                .unwrap_or(false)
    }

    fn uses_map_table(&self, name: &str) -> bool {
        self.properties.values().any(|val| val.uses_map_table(name))
            || self
                .metadata
                .as_ref()
                .map(|val| val.uses_map_table(name))
                .unwrap_or(false)
            || self
                .update_policy
                .as_ref()
                .map(|val| val.uses_map_table(name))
                .unwrap_or(false)
    }
}

impl Inspectable for ResourceIr {
    fn requires_fmt(&self) -> bool {
        match self {
            Self::Sub(_) => true,
            Self::Array(_, list) => list.iter().any(Inspectable::requires_fmt),
            Self::Object(_, props) => props.values().any(Inspectable::requires_fmt),
            Self::Cidr(range, count, mask) => {
                range.requires_fmt() || count.requires_fmt() || mask.requires_fmt()
            }
            Self::GetAZs(region) => region.requires_fmt(),
            Self::If(_, when_true, when_false) => {
                when_true.requires_fmt() || when_false.requires_fmt()
            }
            Self::Join(_, parts) => parts.iter().any(Inspectable::requires_fmt),
            Self::Map(_, tlk, slk) => tlk.requires_fmt() || slk.requires_fmt(),
            Self::Select(_, list) => list.requires_fmt(),
            Self::Split(_, text) => text.requires_fmt(),
            Self::Base64(value) => value.requires_fmt(),
            Self::Null
            | Self::Bool(_)
            | Self::String(_)
            | Self::Number(_)
            | Self::Double(_)
            | Self::Ref(_)
            | Self::ImportValue(_) => false,
        }
    }

    fn requires_time(&self) -> bool {
        match self {
            Self::Array(Structure::Simple(CfnType::Timestamp), ..)
            | Self::Object(Structure::Simple(CfnType::Timestamp), ..) => true,
            Self::Sub(list) => list.iter().any(Inspectable::requires_time),
            Self::Array(_, list) => list.iter().any(Inspectable::requires_time),
            Self::Object(_, props) => props.values().any(Inspectable::requires_time),
            Self::Cidr(range, count, mask) => {
                range.requires_time() || count.requires_time() || mask.requires_time()
            }
            Self::GetAZs(region) => region.requires_time(),
            Self::If(_, when_true, when_false) => {
                when_true.requires_time() || when_false.requires_time()
            }
            Self::Join(_, parts) => parts.iter().any(Inspectable::requires_time),
            Self::Map(_, tlk, slk) => tlk.requires_time() || slk.requires_time(),
            Self::Select(_, list) => list.requires_time(),
            Self::Split(_, text) => text.requires_time(),
            Self::Base64(value) => value.requires_time(),
            Self::Null
            | Self::Bool(_)
            | Self::String(_)
            | Self::Number(_)
            | Self::Double(_)
            | Self::Ref(_)
            | Self::ImportValue(_) => false,
        }
    }

    fn uses_map_table(&self, name: &str) -> bool {
        match self {
            Self::Sub(list) => list.iter().any(|val| val.uses_map_table(name)),
            Self::Array(_, list) => list.iter().any(|val| val.uses_map_table(name)),
            Self::Object(_, props) => props.values().any(|val| val.uses_map_table(name)),
            Self::Cidr(range, count, mask) => {
                range.uses_map_table(name)
                    || count.uses_map_table(name)
                    || mask.uses_map_table(name)
            }
            Self::GetAZs(region) => region.uses_map_table(name),
            Self::If(_, when_true, when_false) => {
                when_true.uses_map_table(name) || when_false.uses_map_table(name)
            }
            Self::Join(_, parts) => parts.iter().any(|val| val.uses_map_table(name)),
            Self::Map(map_name, tlk, slk) => {
                map_name == name || tlk.uses_map_table(name) || slk.uses_map_table(name)
            }
            Self::Select(_, list) => list.uses_map_table(name),
            Self::Split(_, text) => text.uses_map_table(name),
            Self::Base64(value) => value.uses_map_table(name),
            Self::Null
            | Self::Bool(_)
            | Self::String(_)
            | Self::Number(_)
            | Self::Double(_)
            | Self::Ref(_)
            | Self::ImportValue(_) => false,
        }
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
                "String" => "*string".into(),
                other => format!("interface{{/* {other} */}}"),
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
            Self::Ref(reference) => reference.emit_golang(output, indent_lead, None)?,
            Self::Str(str) => output.write_raw(&format!("jsii.String({str:?})"), indent_lead)?,

            Self::And(list) => {
                for (idx, cond) in list.iter().enumerate() {
                    if idx > 0 {
                        output.write_raw(" && ", false)?;
                    }
                    cond.emit_golang(output, indent_lead && idx == 0, None)?;
                }
            }
            Self::Or(list) => {
                for (idx, cond) in list.iter().enumerate() {
                    if idx > 0 {
                        output.write_raw(" || ", false)?;
                    }
                    cond.emit_golang(output, indent_lead && idx == 0, None)?;
                }
            }

            Self::Not(cond) => {
                output.write_raw("!", indent_lead)?;
                cond.emit_golang(output, false, None)?;
            }

            Self::Equals(lhs, rhs) => {
                lhs.emit_golang(output, indent_lead, None)?;
                output.write_raw(" == ", false)?;
                rhs.emit_golang(output, false, None)?
            }

            Self::Map(map, tlk, slk) => {
                output.write_raw(
                    &golang_identifier(map, IdentifierKind::Unexported),
                    indent_lead,
                )?;
                output.write_raw("[", false)?;
                tlk.emit_golang(output, false, None)?;
                output.write_raw("][", false)?;
                slk.emit_golang(output, false, None)?;
                output.write_raw("]", false)?;
            }
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
                        name => format!("*{name} /* FIXME */").into(),
                    },
                    Structure::Simple(simple) => match simple {
                        CfnType::Boolean => "*bool".into(),
                        CfnType::Double | CfnType::Integer | CfnType::Long => "*float64".into(),
                        CfnType::Json => "interface{}".into(),
                        CfnType::String => "*string".into(),
                        CfnType::Timestamp => "time.Time".into(),
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
                        "Tag" => output.write_raw_line("&cdk.CfnTag{", indent_lead)?,
                        name => {
                            output.write_raw_line(&format!("&{name}/* FIXME */{{"), indent_lead)?;
                        }
                    },
                    Structure::Simple(cfn) => {
                        unreachable!("object with simple structure ({:?})", cfn)
                    }
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
                match mask.as_ref() {
                    ResourceIr::Number(mask) => {
                        output.write_raw(&format!("jsii.String(\"{mask}\")"), false)?;
                    }
                    ResourceIr::String(mask) => {
                        output.write_raw(&format!("jsii.String({mask:?})"), false)?;
                    }
                    mask => {
                        output.write_raw("jsii.String(fmt.Sprintf(\"%v\", ", false)?;
                        mask.emit_golang(output, false, None)?;
                        output.write_raw("))", false)?;
                    }
                }
                output.write_raw(")", false)?;
            }
            Self::GetAZs(region) => {
                output.write_raw("cdk.Fn_GetAzs(", indent_lead)?;
                region.emit_golang(output, false, None)?;
                output.write_raw(")", false)?;
            }
            Self::If(cond, when_true, when_false) => {
                output.write_raw_line(
                    "func() interface{} { // TODO: fix to appropriate value type",
                    indent_lead,
                )?;
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
            Self::Split(sep, str) => {
                output.write_raw(&format!("cdk.Fn_Split(jsii.String({sep:?}), "), indent_lead)?;
                str.emit_golang(output, false, None)?;
                output.write_raw(")", false)?;
            }
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
            Origin::Condition => output.write_raw(
                &golang_identifier(&self.name, IdentifierKind::Unexported),
                indent_lead,
            )?,
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
    /// The identifier is exported. It'll be named using PascalCase.
    Exported,
    /// The identifier is unexported. It'll be named using camelCase.
    Unexported,
    /// The identifier is a module symbol. It'll be named using snake_case.
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
