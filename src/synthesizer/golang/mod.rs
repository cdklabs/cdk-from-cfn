#![allow(unused_variables)]

use crate::code::{CodeBuffer, IndentOptions};
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
use std::rc::Rc;
use voca_rs::case::{camel_case, pascal_case, snake_case};

use super::Synthesizer;

const INDENT: Cow<'static, str> = Cow::Borrowed("\t");
const TERNARY: &str = "ifCondition";

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
    fn synthesize(
        &self,
        ir: CloudformationProgramIr,
        into: &mut dyn io::Write,
        stack_name: &str,
    ) -> io::Result<()> {
        let code = CodeBuffer::default();

        code.line(format!("package {}", self.package_name));
        code.newline();

        let imports = code.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some("import (".into()),
            trailing: Some(")".into()),
            trailing_newline: true,
        });
        let stdlib_imports = imports.section(false);

        for import in &ir.imports {
            imports.line(import.to_golang());
        }
        // The usual imports of constructs library & jsii runtime
        imports.line("\"github.com/aws/constructs-go/constructs/v10\"");
        imports.line("\"github.com/aws/jsii-runtime-go\"");

        code.newline();

        let props = code.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some(format!("type {}Props struct {{", stack_name).into()),
            trailing: Some("}".into()),
            trailing_newline: true,
        });
        props.line("cdk.StackProps"); // Extends cdk.StackProps
        for param in &ir.constructor.inputs {
            if let Some(description) = &param.description {
                props.indent("/// ".into()).line(description.to_owned());
            }
            props.line(param.to_golang_field());
        }
        code.newline();

        if let Some(description) = &ir.description {
            code.indent("/// ".into()).line(description.to_owned());
        }
        let class = code.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some(format!("type {} struct {{", stack_name).into()),
            trailing: Some("}".into()),
            trailing_newline: true,
        });
        class.line("cdk.Stack");
        for output in &ir.outputs {
            if let Some(description) = &output.description {
                class.indent("/// ".into()).line(description.to_owned());
            }
            class.line(format!(
                "{name} interface{{}} // TODO: fix to appropriate type",
                name = golang_identifier(&output.name, IdentifierKind::Exported)
            ));
        }
        code.newline();

        let ctor = code.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some(
                format!(
                    "func New{}(scope constructs.Construct, id string, props {}Props) *{} {{",
                    stack_name, stack_name, stack_name
                )
                .into(),
            ),
            trailing: Some("}".into()),
            trailing_newline: true,
        });

        let context = &mut {
            let fmt = stdlib_imports.section(false);
            let time = stdlib_imports.section(false);
            let blank = stdlib_imports.section(false);
            let ternary = code.section(false);
            GoContext::new(fmt, time, blank, ternary)
        };

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
                ctor.line("/*");
            }
            let map = ctor.indent_with_options(IndentOptions {
                indent: INDENT,
                leading: Some(
                    format!(
                        "{} := map[*string]map[*string]{leaf_type}{{",
                        golang_identifier(&mapping.name, IdentifierKind::Unexported)
                    )
                    .into(),
                ),
                trailing: Some("}".into()),
                trailing_newline: true,
            });
            for (key, inner) in &mapping.map {
                let inner_map = map.indent_with_options(IndentOptions {
                    indent: INDENT,
                    leading: Some(
                        format!("jsii.String({key:?}): map[*string]{leaf_type}{{").into(),
                    ),
                    trailing: Some("},".into()),
                    trailing_newline: true,
                });
                for (key, value) in inner {
                    inner_map.text(format!("jsii.String({key:?}): "));
                    match value {
                        MappingInnerValue::Bool(bool) => {
                            inner_map.text(format!("jsii.Bool({bool})"))
                        }
                        MappingInnerValue::Number(num) => {
                            inner_map.text(format!("jsii.Number({num})"))
                        }
                        MappingInnerValue::Float(num) => {
                            inner_map.text(format!("jsii.Number({num})"))
                        }
                        MappingInnerValue::String(str) => {
                            inner_map.text(format!("jsii.String({str:?})"))
                        }
                        MappingInnerValue::List(items) => {
                            let list = inner_map.indent_with_options(IndentOptions {
                                indent: INDENT,
                                leading: Some("[]*string{".into()),
                                trailing: Some("}".into()),
                                trailing_newline: false,
                            });
                            for item in items {
                                list.line(format!("jsii.String({item:?}),"));
                            }
                        }
                    }
                    inner_map.line(",");
                }
            }
            if !used {
                ctor.line("*/");
            }
            ctor.newline();
        }

        ctor.line("stack := cdk.NewStack(scope, &id, &props.StackProps)");
        ctor.newline();

        for condition in &ir.conditions {
            ctor.text(format!(
                "{name} := ",
                name = golang_identifier(&condition.name, IdentifierKind::Unexported)
            ));
            condition.value.emit_golang(context, &ctor, None);
            ctor.newline();
            ctor.newline();
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
            let params = ctor.indent_with_options(IndentOptions {
                indent: INDENT,
                leading: Some(format!("{prefix}{ns}.NewCfn{class}(").into()),
                trailing: Some(")".into()),
                trailing_newline: true,
            });
            params.line("stack,");
            params.line(format!("jsii.String({:?}),", resource.name));
            let props = params.indent_with_options(IndentOptions {
                indent: INDENT,
                leading: Some(format!("&{ns}.Cfn{class}Props{{").into()),
                trailing: Some("},".into()),
                trailing_newline: true,
            });
            for (name, value) in &resource.properties {
                props.text(format!(
                    "{}: ",
                    golang_identifier(name, IdentifierKind::Exported)
                ));
                value.emit_golang(context, &props, None);
                props.line(",");
            }
            ctor.newline();
        }

        for output in &ir.outputs {
            if let Some(export) = &output.export {
                let props = ctor.indent_with_options(IndentOptions {
                    indent: INDENT,
                    leading: Some(
                        format!(
                            "cdk.NewCfnOutput(stack, jsii.String({name:?}), &cdk.CfnOutputProps{{",
                            name = output.name
                        )
                        .into(),
                    ),
                    trailing: Some("})".into()),
                    trailing_newline: true,
                });
                if let Some(description) = &output.description {
                    props.line(format!("Description: jsii.String({description:?}),"));
                }
                props.text("ExportName: ");
                export.emit_golang(context, &props, Some(","));
                props.text("Value: ");
                output.value.emit_golang(context, &props, Some(","));
                ctor.newline();
            }
        }

        let fields = ctor.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some(format!("return &{}{{", stack_name).into()),
            trailing: Some("}".into()),
            trailing_newline: true,
        });
        fields.line("Stack: stack,");
        for output in &ir.outputs {
            fields.text(format!(
                "{name}: ",
                name = golang_identifier(&output.name, IdentifierKind::Exported)
            ));
            output.value.emit_golang(context, &fields, None);
            fields.line(",");
        }

        code.write(into)
    }
}

struct GoContext {
    fmt: Rc<CodeBuffer>,
    time: Rc<CodeBuffer>,
    blank: Rc<CodeBuffer>,
    ternary: Rc<CodeBuffer>,
    has_fmt: bool,
    has_time: bool,
    has_blank: bool,
    has_ternary: bool,
}
impl GoContext {
    const fn new(
        fmt: Rc<CodeBuffer>,
        time: Rc<CodeBuffer>,
        blank: Rc<CodeBuffer>,
        ternary: Rc<CodeBuffer>,
    ) -> Self {
        Self {
            fmt,
            time,
            blank,
            ternary,
            has_fmt: false,
            has_time: false,
            has_blank: false,
            has_ternary: false,
        }
    }

    fn import_fmt(&mut self) {
        if self.has_fmt {
            return;
        }
        self.fmt.line("\"fmt\"");
        self.has_fmt = true;

        self.insert_blank();
    }

    fn import_time(&mut self) {
        if self.has_time {
            return;
        }
        self.time.line("\"time\"");
        self.has_time = true;

        self.insert_blank();
    }

    fn insert_blank(&mut self) {
        if self.has_blank {
            return;
        }
        self.blank.newline();
        self.has_blank = true;
    }

    fn insert_ternary(&mut self) {
        if self.has_ternary {
            return;
        }

        self.ternary.newline();
        let comment = self.ternary.indent("/// ".into());
        comment.line("ifCondition is a helper function that replicates the ternary");
        comment.line("operator that can be found in other languages. It is conceptually");
        comment.line("equivalent to writing `cond ? whenTrue : whenFalse`, meaning it");
        comment.line("returns `whenTrue` if `cond` is `true`, and `whenFalse` otherwise.");
        let block = self.ternary.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some(
                format!("func {TERNARY}[T any](cond bool, whenTrue T, whenFalse T) T {{").into(),
            ),
            trailing: Some("}".into()),
            trailing_newline: true,
        });

        block
            .indent_with_options(IndentOptions {
                indent: INDENT,
                leading: Some("if cond {".into()),
                trailing: Some("}".into()),
                trailing_newline: true,
            })
            .line("return whenTrue");
        block.line("return whenFalse");

        self.has_ternary = true;
    }
}

trait Inspectable {
    /// Whether the rendered code for this entity uses the named mapping table.
    fn uses_map_table(&self, name: &str) -> bool;
}

impl Inspectable for CloudformationProgramIr {
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
    fn uses_map_table(&self, name: &str) -> bool {
        match self {
            ConditionIr::Equals(lhs, rhs) => lhs.uses_map_table(name) || rhs.uses_map_table(name),
            ConditionIr::Not(cond) => cond.uses_map_table(name),
            ConditionIr::And(list) | ConditionIr::Or(list) => {
                list.iter().any(|cond| cond.uses_map_table(name))
            }
            ConditionIr::Map(map_name, _, _) => map_name == name,
            ConditionIr::Condition(_) | ConditionIr::Str(_) | ConditionIr::Ref(_) => false,
            ConditionIr::Split(_, cond) => cond.uses_map_table(name),
            ConditionIr::Select(_, cond) => cond.uses_map_table(name),
        }
    }
}

impl Inspectable for ResourceInstruction {
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
    fn emit_golang(&self, context: &mut GoContext, output: &CodeBuffer, trailer: Option<&str>);
}

impl GolangEmitter for ConditionIr {
    fn emit_golang(&self, context: &mut GoContext, output: &CodeBuffer, trailer: Option<&str>) {
        match self {
            Self::Ref(reference) => reference.emit_golang(context, output, None),
            Self::Str(str) => output.text(format!("jsii.String({str:?})")),
            Self::Condition(x) => output.text(golang_identifier(x, IdentifierKind::Unexported)),

            Self::And(list) => {
                for (idx, cond) in list.iter().enumerate() {
                    if idx > 0 {
                        output.text(" && ");
                    }
                    cond.emit_golang(context, output, None);
                }
            }
            Self::Or(list) => {
                for (idx, cond) in list.iter().enumerate() {
                    if idx > 0 {
                        output.text(" || ");
                    }
                    cond.emit_golang(context, output, None);
                }
            }

            Self::Not(cond) => {
                output.text("!");
                cond.emit_golang(context, output, None);
            }

            Self::Equals(lhs, rhs) => {
                lhs.emit_golang(context, output, None);
                output.text(" == ");
                rhs.emit_golang(context, output, None)
            }

            Self::Map(map, tlk, slk) => {
                output.text(golang_identifier(map, IdentifierKind::Unexported));
                output.text("[");
                tlk.emit_golang(context, output, None);
                output.text("][");
                slk.emit_golang(context, output, None);
                output.text("]");
            }
            ConditionIr::Split(sep, str) => {
                output.text(format!("cdk.Fn_Split(jsii.String({sep:?}), "));
                str.emit_golang(context, output, None);
                output.text(")");
            }
            ConditionIr::Select(index, str) => {
                output.text(format!("cdk.Fn_Select(jsii.Number({index:?}), "));
                str.emit_golang(context, output, None);
                output.text(")");
            }
        }
        if let Some(trailer) = trailer {
            output.text(trailer.to_owned())
        }
    }
}

impl GolangEmitter for ResourceIr {
    fn emit_golang(&self, context: &mut GoContext, output: &CodeBuffer, trailer: Option<&str>) {
        match self {
            // Canonical nil
            Self::Null => output.text("nil"),

            // Literal values
            Self::Bool(bool) => output.text(format!("jsii.Bool({bool})")),
            Self::Double(double) => {
                output.text(format!("jsii.Number({double})"));
            }
            Self::Number(number) => {
                output.text(format!("jsii.Number({number})"));
            }
            Self::String(text) => {
                output.text(format!("jsii.String({text:?})"));
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
                        CfnType::Timestamp => {
                            context.import_time();
                            "time.Time".into()
                        }
                    },
                };

                let items = output.indent_with_options(IndentOptions {
                    indent: INDENT,
                    leading: Some(format!("&[]{value_type}{{").into()),
                    trailing: Some("}".into()),
                    trailing_newline: false,
                });
                for item in array {
                    item.emit_golang(context, &items, None);
                    items.line(",");
                }
            }
            Self::Object(structure, properties) => {
                let mut structure_is_simple_json = false;
                let props = output.indent_with_options(IndentOptions {
                    indent: INDENT,
                    leading: Some(match structure {
                        Structure::Composite(name) => match *name {
                            "Tag" => "&cdk.CfnTag{".into(),
                            name => format!("&{name}/* FIXME */{{").into(),
                        },
                        Structure::Simple(cfn) => match cfn {
                            CfnType::Json => {
                                structure_is_simple_json = true;
                                "map[string]interface{} {".into()
                            }
                            _ => unreachable!("object with simple structure ({:?})", cfn)
                        }
                    }),
                    trailing: Some("}".into()),
                    trailing_newline: false,
                });
                for (name, val) in properties {
                    if structure_is_simple_json { 
                        props.text(format!(
                            "\"{name}\": ",
                            name = golang_identifier(name, IdentifierKind::Exported)
                        ));
                    } else {
                        props.text(format!(
                            "{name}: ",
                            name = golang_identifier(name, IdentifierKind::Exported)
                        ));
                    } 
                    val.emit_golang(context, &props, Some(","));
                }
            }

            // Intrinsic functions
            Self::Base64(value) => {
                output.text("cdk.Fn_Base64(");
                value.emit_golang(context, output, None);
                output.text(")");
            }
            Self::Cidr(cidr_block, count, mask) => {
                output.text("cdk.Fn_Cidr(");
                cidr_block.emit_golang(context, output, None);
                output.text(", ");
                count.emit_golang(context, output, None);
                output.text(", ");
                match mask.as_ref() {
                    ResourceIr::Number(mask) => {
                        output.text(format!("jsii.String(\"{mask}\")"));
                    }
                    ResourceIr::String(mask) => {
                        output.text(format!("jsii.String({mask:?})"));
                    }
                    mask => {
                        context.import_fmt();
                        output.text("jsii.String(fmt.Sprintf(\"%v\", ");
                        mask.emit_golang(context, output, None);
                        output.text("))");
                    }
                }
                output.text(")");
            }
            Self::GetAZs(region) => {
                output.text("cdk.Fn_GetAzs(");
                region.emit_golang(context, output, None);
                output.text(")");
            }
            Self::If(cond, when_true, when_false) => {
                // Ensure the ternary function is there...
                context.insert_ternary();

                let call = output.indent_with_options(IndentOptions {
                    indent: INDENT,
                    leading: Some(format!("{TERNARY}(").into()),
                    trailing: Some(")".into()),
                    trailing_newline: false,
                });
                call.line(format!(
                    "{cond},",
                    cond = golang_identifier(cond, IdentifierKind::Unexported)
                ));
                when_true.emit_golang(context, &call, Some(","));
                when_false.emit_golang(context, &call, Some(","));
            }
            Self::ImportValue(import) => {
                output.text(format!("cdk.Fn_ImportValue(jsii.String({import:?}))"))
            }
            Self::Join(sep, list) => {
                let items = output.indent_with_options(IndentOptions {
                    indent: INDENT,
                    leading: Some(format!("cdk.Fn_Join(jsii.String({sep:?}), &[]*string{{").into()),
                    trailing: Some("})".into()),
                    trailing_newline: false,
                });
                for item in list {
                    item.emit_golang(context, &items, Some(","));
                }
            }
            Self::Map(table, tlk, slk) => {
                output.text(format!(
                    "{table}[",
                    table = golang_identifier(table, IdentifierKind::Unexported)
                ));
                tlk.emit_golang(context, output, None);
                output.text("][");
                slk.emit_golang(context, output, None);
                output.text("]");
            }
            Self::Select(idx, list) => match list.as_ref() {
                ResourceIr::Array(_, items) => {
                    items[*idx].emit_golang(context, output, None);
                }
                list => {
                    output.text(format!("cdk.Fn_Select(jsii.Number({idx}), "));
                    list.emit_golang(context, output, None);
                    output.text(")");
                }
            },
            Self::Split(sep, str) => {
                output.text(format!("cdk.Fn_Split(jsii.String({sep:?}), "));
                str.emit_golang(context, output, None);
                output.text(")");
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
                context.import_fmt();
                output.text(format!("jsii.String(fmt.Sprintf({pattern:?}"));
                for part in parts {
                    match part {
                        ResourceIr::Bool(_)
                        | ResourceIr::Double(_)
                        | ResourceIr::Number(_)
                        | ResourceIr::String(_) => {}
                        part => {
                            output.text(", ");
                            part.emit_golang(context, output, None);
                        }
                    }
                }
                output.text("))");
            }

            // References
            Self::Ref(reference) => reference.emit_golang(context, output, None),
        }

        if let Some(trailer) = trailer {
            output.line(trailer.to_owned())
        }
    }
}

impl GolangEmitter for Reference {
    fn emit_golang(&self, context: &mut GoContext, output: &CodeBuffer, trailer: Option<&str>) {
        match &self.origin {
            Origin::Condition => {
                output.text(golang_identifier(&self.name, IdentifierKind::Unexported))
            }
            Origin::GetAttribute {
                attribute,
                conditional,
            } => output.text(format!(
                "{name}.Attr{attribute}()",
                name = golang_identifier(&self.name, IdentifierKind::Unexported),
                attribute = golang_identifier(attribute, IdentifierKind::Exported),
            )),
            Origin::LogicalId { conditional } => output.text(format!(
                "{name}.Ref()",
                name = golang_identifier(&self.name, IdentifierKind::Unexported)
            )),
            Origin::Parameter => output.text(format!(
                "props.{name}",
                name = golang_identifier(&self.name, IdentifierKind::Exported)
            )),
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
                output.text(format!("stack.{pseudo}()"));
            }
        }

        if let Some(trailer) = trailer {
            output.line(trailer.to_owned())
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
