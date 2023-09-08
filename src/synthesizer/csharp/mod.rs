use crate::code::{CodeBuffer, IndentOptions};
use crate::ir::conditions::ConditionIr;
use crate::ir::constructor::ConstructorParameter;
use crate::ir::importer::ImportInstruction;
use crate::ir::mappings::OutputType;
use crate::ir::outputs::OutputInstruction;
use crate::ir::reference::{Origin, PseudoParameter, Reference};
use crate::ir::resources::ResourceIr;
use crate::ir::CloudformationProgramIr;
use crate::parser::lookup_table::MappingInnerValue;
use crate::specification::{CfnType, Structure};
use std::borrow::Cow;
use std::io;
use voca_rs::case::{camel_case, pascal_case};

use super::Synthesizer;

const INDENT: Cow<'static, str> = Cow::Borrowed("    ");

pub struct CSharp {
    namespace: String,
}

impl CSharp {
    pub fn new(namespace: impl Into<String>) -> Self {
        Self {
            namespace: namespace.into(),
        }
    }
}

impl Default for CSharp {
    fn default() -> Self {
        Self::new("Com.Acme.Test.Simple")
    }
}

impl Synthesizer for CSharp {
    fn synthesize(
        &self,
        ir: CloudformationProgramIr,
        into: &mut dyn io::Write,
        stack_name: &str,
    ) -> io::Result<()> {
        // Initialize the code buffer in which all of the code will be generated
        let code = CodeBuffer::default();

        // Imports
        for import in &ir.imports {
            code.line(import.to_csharp())
        }
        code.line("using Constructs;");
        code.line("using System.Collections.Generic;");
        code.newline();

        // Namespace definition
        let namespace = code.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some(format!("namespace {}\n{{", self.namespace).into()),
            trailing: Some("}".into()),
            trailing_newline: true,
        });

        // Props
        let stack_props_class = namespace.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some(format!("public class {stack_name}Props : StackProps\n{{").into()),
            trailing: Some("}".into()),
            trailing_newline: true,
        });

        for param in &ir.constructor.inputs {
            if let Some(description) = &param.description {
                stack_props_class.line("/// <summary>");
                for description_line in description.split('\n') {
                    stack_props_class.line(format!("/// {description_line}"));
                }
                stack_props_class.line("/// </summary>");
            }
            stack_props_class.line(param.to_csharp_auto_property());
            stack_props_class.newline();
        }

        namespace.newline();

        // Description - comment before the stack class
        if let Some(descr) = ir.description {
            namespace.line("/// <summary>");
            for description_line in descr.split('\n') {
                namespace.line(format!("/// {description_line}"));
            }
            namespace.line("/// </summary>");
        }

        // Stack class definition
        let stack_class = namespace.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some(format!("public class {stack_name} : Stack\n{{").into()),
            trailing: Some("}".into()),
            trailing_newline: true,
        });

        // Properties for each output
        for output in &ir.outputs {
            if let Some(description) = &output.description {
                stack_class.line("/// <summary>");
                for description_line in description.split('\n') {
                    stack_class.line(format!("/// {description_line}"));
                }
                stack_class.line("/// </summary>");
            }
            stack_class.line(format!("public object {} {{ get; }} ", output.name));
            stack_class.newline();
        }

        // Constructor
        let ctor = stack_class.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some(format!(
                "public {}(Construct scope, string id, {}Props props = null) : base(scope, id, props)\n{{",
                stack_name,
                stack_name
            ).into()),
            trailing: Some("}".into()),
            trailing_newline: true,
        });

        // Default values for input props
        let have_default_or_special_type_params = &ir
            .constructor
            .inputs
            .iter()
            .filter(|p| p.constructor_type.contains("AWS::") || p.default_value.is_some())
            .collect::<Vec<&ConstructorParameter>>();
        if !have_default_or_special_type_params.is_empty() {
            ctor.line("// Applying default props");
            for param in have_default_or_special_type_params {
                let name = pascal_case(&param.name);
                // example: AWS::EC2::Image::Id, List<AWS::EC2::VPC::Id>, AWS::SSM::Parameter::Value<List<String>>
                if param.constructor_type.contains("AWS::") {
                    let value_as = match &param.constructor_type {
                        t if t.contains("List") => "ValueAsList",
                        _ => "ValueAsString",
                    };
                    let cfn_param = ctor.indent_with_options(IndentOptions {
                        indent: INDENT,
                        leading: Some(
                            format!(
                                "props.{name} = new CfnParameter(this, \"{name}\", new CfnParameterProps\n{{")
                            .into(),
                        ),
                        trailing: Some(format!("}}).{value_as};").into()),
                        trailing_newline: true,
                    });
                    cfn_param.line(format!("Type = \"{}\",", param.constructor_type));
                    let cfn_param_default_pre = match &param.constructor_type {
                        t if t.contains("List") => "string.Join(\",\", ",
                        _ => "",
                    };
                    let cfn_param_default_post = match &param.constructor_type {
                        t if t.contains("List") => ")",
                        _ => "",
                    };
                    if let Some(v) = &param.default_value {
                        cfn_param.line(format!(
                            "Default = {cfn_param_default_pre}props.{name}{cfn_param_default_post} ?? \"{}\",",
                            v.escape_debug()
                        ));
                    } else {
                        cfn_param.line(format!("Default = {cfn_param_default_pre}props.{name}{cfn_param_default_post},"));
                    };
                    if let Some(v) = &param.description {
                        cfn_param.line(format!("Description = \"{}\",", v));
                    };
                } else {
                    let value = match &param.default_value {
                        None => "".to_owned(),
                        Some(value) => {
                            let value = match param.constructor_type.as_str() {
                                "String" => format!("\"{}\"", value.escape_debug()),
                                "List<Number>" => format!("[{value}]"),
                                "CommaDelimitedList" => format!(
                                    "[{}]",
                                    value
                                        .split(',')
                                        .map(|v| format!("\"{}\"", v.escape_debug()))
                                        .collect::<Vec<String>>()
                                        .join(",")
                                ),
                                _ => value.clone(),
                            };
                            value
                        }
                    };

                    ctor.line(format!("props.{name} ??= {value};"));
                };
            }
            ctor.newline();
        }

        // Mappings
        if !ir.mappings.is_empty() {
            ctor.line("// Mappings");
        }
        for mapping in &ir.mappings {
            let leaf_type = match mapping.output_type() {
                OutputType::Complex => "object",
                OutputType::Consistent(inner) => match inner {
                    MappingInnerValue::Bool(_) => "bool",
                    MappingInnerValue::Float(_) => "double",
                    MappingInnerValue::Number(_) => "int",
                    MappingInnerValue::String(_) => "string",
                    MappingInnerValue::List(_) => "string[]",
                },
            };

            let map = ctor.indent_with_options(IndentOptions {
                indent: INDENT,
                leading: Some(
                    format!(
                        "var {} = new Dictionary<string, Dictionary<string,{leaf_type}>> \n{{",
                        camel_case(&mapping.name)
                    )
                    .into(),
                ),
                trailing: Some("};".into()),
                trailing_newline: true,
            });

            for (key, inner) in &mapping.map {
                let map_item = map.indent_with_options(IndentOptions {
                    indent: INDENT,
                    leading: Some(
                        format!("[\"{key}\"] = new Dictionary<string, {leaf_type}>\n{{").into(),
                    ),
                    trailing: Some("},".into()),
                    trailing_newline: true,
                });

                for (inner_key, inner_value) in inner {
                    match inner_value {
                        MappingInnerValue::Bool(_)
                        | MappingInnerValue::Float(_)
                        | MappingInnerValue::Number(_) => {
                            map_item.text(format!("[\"{inner_key}\"] = {inner_value},"));
                        }
                        MappingInnerValue::String(s) => {
                            map_item.text(format!("[\"{inner_key}\"] = \"{s}\","));
                        }
                        MappingInnerValue::List(l) => {
                            let list = map_item.indent_with_options(IndentOptions {
                                indent: INDENT,
                                leading: Some(
                                    format!("[\"{inner_key}\"] = new string[] \n{{").into(),
                                ),
                                trailing: Some("},".into()),
                                trailing_newline: true,
                            });
                            for list_item in l {
                                list.line(format!("\"{list_item}\","));
                            }
                        }
                    }
                    map_item.newline();
                }
            }
        }

        // Conditions
        if !ir.conditions.is_empty() {
            ctor.newline();
            ctor.line("// Conditions");
        }
        for condition in &ir.conditions {
            ctor.text(format!("bool {} = ", camel_case(&condition.name)));
            condition.value.emit_csharp(&ctor);
            ctor.text(";");
            ctor.newline();
        }

        // Resources
        ctor.newline();
        ctor.line("// Resources");
        for resource in &ir.resources {
            let class = resource.resource_type.type_name();
            let resource_constructor = ctor.indent_with_options(IndentOptions {
                indent: INDENT,
                leading: Some(format!("var {var_name} = new Cfn{class}(this, \"{construct_id}\", new Cfn{class}Props\n{{", 
                    var_name = camel_case(&resource.name),
                    construct_id = resource.name,
                ).into()),
                trailing: Some("});".into()),
                trailing_newline: true,
            });
            for (name, value) in &resource.properties {
                resource_constructor.text(format!("{name} = "));
                value.emit_csharp(&resource_constructor, Some(class));
                resource_constructor.text(",");
                resource_constructor.newline();
            }
        }

        // Set values for the outputs
        if !ir.outputs.is_empty() {
            ctor.newline();
            ctor.line("// Outputs");

            for op in &ir.outputs {
                op.emit_csharp(&ctor);
            }
        }

        code.write(into)
    }
}

impl ImportInstruction {
    fn to_csharp(&self) -> String {
        let mut parts: Vec<Cow<str>> = vec![match self.path[0].as_str() {
            "aws-cdk-lib" => "Amazon.CDK".into(),
            other => other.into(),
        }];

        if self.path.len() > 1 {
            for submodule_part in self.path[1].split('-') {
                parts.push(match submodule_part {
                    "aws" => "AWS".into(),
                    // TODO - This is hardcoded for now.
                    // This part of the namespace needs to be pulled from the jsiirc.json
                    // of the submodule. In C# there is no consistent rule we can apply to transform
                    // this string to have the right casing.
                    // Some are all caps, and some are Pascal case.
                    "s3" => "S3".into(),
                    "sqs" => "SQS".into(),
                    "ec2" => "EC2".into(),
                    other => other.into(),
                });
            }
        }

        let namespace = parts.join(".");

        format!("using {namespace};")
    }
}

impl ConstructorParameter {
    fn to_csharp_auto_property(&self) -> String {
        let prop_type = match &self.constructor_type {
            t if t.contains("List") => "string[]",
            _ => "string",
        };

        format!(
            "public {prop_type} {} {{ get; set; }}",
            pascal_case(&self.name)
        )
    }
}

trait CsharpEmitter {
    fn emit_csharp(&self, output: &CodeBuffer);
}

impl CsharpEmitter for ConditionIr {
    fn emit_csharp(&self, output: &CodeBuffer) {
        match self {
            ConditionIr::Ref(reference) => reference.emit_csharp(output),
            ConditionIr::Str(str) => output.text(format!("\"{str}\"")),
            ConditionIr::Condition(condition) => output.text(camel_case(condition)),

            ConditionIr::And(list) => {
                for (index, condition) in list.iter().enumerate() {
                    if index > 0 {
                        output.text(" && ");
                    }
                    condition.emit_csharp(output);
                }
            }
            ConditionIr::Or(list) => {
                for (index, condition) in list.iter().enumerate() {
                    if index > 0 {
                        output.text(" || ");
                    }
                    condition.emit_csharp(output);
                }
            }

            ConditionIr::Not(condition) => {
                output.text("!");
                condition.emit_csharp(output);
            }

            ConditionIr::Equals(left, right) => {
                left.emit_csharp(output);
                output.text(" == ");
                right.emit_csharp(output);
            }

            ConditionIr::Map(map, top_level_key, second_level_key) => {
                output.text(camel_case(map));
                output.text("[");
                top_level_key.emit_csharp(output);
                output.text("][");
                second_level_key.emit_csharp(output);
                output.text("]");
            }
            ConditionIr::Split(sep, str) => {
                output.text(format!("Fn.Split(\"{sep}\", "));
                str.emit_csharp(output);
                output.text(")");
            }
            ConditionIr::Select(index, str) => {
                output.text(format!("Fn.Select({index}, "));
                str.emit_csharp(output);
                output.text(")");
            }
        }
    }
}

impl CsharpEmitter for Reference {
    fn emit_csharp(&self, output: &CodeBuffer) {
        match &self.origin {
            Origin::Condition => output.text(camel_case(&self.name)),
            Origin::GetAttribute {
                attribute,
                conditional: _,
            } => output.text(format!("{}.Attr{attribute}", camel_case(&self.name))),
            Origin::LogicalId { conditional: _ } => {
                output.text(format!("{}.Ref", camel_case(&self.name)))
            }
            Origin::Parameter => output.text(format!("props.{}", pascal_case(&self.name))),
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
                output.text(pseudo);
            }
        }
    }
}

impl ResourceIr {
    fn emit_csharp(&self, output: &CodeBuffer, root_resource: Option<&str>) {
        match self {
            ResourceIr::Null => output.text("null"),
            ResourceIr::Bool(bool) => output.text(bool.to_string()),
            ResourceIr::Number(number) => output.text(number.to_string()),
            ResourceIr::Double(double) => output.text(double.to_string()),
            ResourceIr::String(str) => output.text(format!("\"{str}\"")),

            ResourceIr::Array(_structure, array) => {
                let array_block = output.indent_with_options(IndentOptions {
                    indent: INDENT,
                    leading: Some("new []\n{".into()),
                    trailing: Some("}".into()),
                    trailing_newline: false,
                });
                for item in array {
                    item.emit_csharp(&array_block, root_resource);
                    array_block.text(",");
                    array_block.newline();
                }
            }
            ResourceIr::Object(structure, properties) => {
                let object_block = output.indent_with_options(IndentOptions {
                    indent: INDENT,
                    leading: Some(match structure {
                        Structure::Composite(name) => match *name {
                            "Tag" => "new CfnTag\n{".into(),
                            name => match root_resource {
                                Some(r) => format!("new Cfn{r}.{name}Property\n{{").into(),
                                None => unreachable!("cannot emit ResourceIr::Object without a parent resource type")
                            }
                        }
                        Structure::Simple(cfn) => match cfn {
                            CfnType::Json => "new Dictionary<string, object>\n{".into(),
                            _ => unreachable!("cannot emit ResourceIr::Object with non-json simple structure ({:?})", cfn)
                        }
                    }),
                    trailing: Some("}".into()),
                    trailing_newline: false,
                });

                for (name, val) in properties {
                    object_block.text(match structure {
                        Structure::Composite(_) => format!("{name} = "),
                        Structure::Simple(_) => format!("{{ \"{name}\", "),
                    });
                    match val {
                        ResourceIr::Bool(_) | ResourceIr::Number(_) | ResourceIr::Double(_) => {
                            object_block.text("\"");
                            val.emit_csharp(&object_block, root_resource);
                            object_block.text("\"");
                        }
                        _ => val.emit_csharp(&object_block, root_resource),
                    }
                    object_block.text(match structure {
                        Structure::Composite(_) => ",",
                        Structure::Simple(_) => "},",
                    });
                    object_block.newline();
                }
            }

            ResourceIr::If(cond, when_true, when_false) => {
                output.text(format!("{} ? ", camel_case(cond)));
                when_true.emit_csharp(output, root_resource);
                output.text(" : ");
                when_false.emit_csharp(output, root_resource);
            }
            ResourceIr::Join(sep, list) => {
                let items = output.indent_with_options(IndentOptions {
                    indent: INDENT,
                    leading: Some(format!("string.Join(\"{sep}\", new []\n{{").into()),
                    trailing: Some("})".into()),
                    trailing_newline: false,
                });
                for item in list {
                    item.emit_csharp(&items, root_resource);
                    items.text(",");
                    items.newline();
                }
            }
            ResourceIr::Split(sep, str) => {
                output.text(format!("Fn.Split(\"{sep}\", "));
                str.emit_csharp(output, root_resource);
                output.text(")");
            }
            ResourceIr::Ref(reference) => reference.emit_csharp(output),
            ResourceIr::Sub(parts) => {
                output.text("$\"");
                for part in parts {
                    match part {
                        ResourceIr::String(lit) => output.text(lit.clone()),
                        other => {
                            output.text("{");
                            other.emit_csharp(output, root_resource);
                            output.text("}");
                        }
                    }
                }
                output.text("\"")
            }
            ResourceIr::Map(table, top_level_key, second_level_key) => {
                //Factor out shared code
                output.text(camel_case(table));
                output.text("[");
                top_level_key.emit_csharp(output, root_resource);
                output.text("][");
                second_level_key.emit_csharp(output, root_resource);
                output.text("]");
            }
            ResourceIr::Base64(value) => {
                output.text("Fn.Base64(");
                value.emit_csharp(output, root_resource);
                output.text(" as string)");
            }
            ResourceIr::ImportValue(import) => {
                output.text(format!("Fn.ImportValue(\"{import}\")"));
            }
            ResourceIr::GetAZs(region) => {
                output.text("Fn.GetAzs(");
                region.emit_csharp(output, root_resource);
                output.text(")");
            }
            ResourceIr::Select(idx, list) => match list.as_ref() {
                ResourceIr::Array(_, array) => {
                    if *idx <= array.len() {
                        array[*idx].emit_csharp(output, root_resource);
                    } else {
                        output.text("null")
                    }
                }
                other => {
                    output.text(format!("Fn.Select({idx}, "));
                    other.emit_csharp(output, root_resource);
                    output.text(")")
                }
            },
            ResourceIr::Cidr(cidr_block, count, mask) => {
                output.text("Fn.Cidr(");
                cidr_block.emit_csharp(output, root_resource);
                output.text(", ");
                count.emit_csharp(output, root_resource);
                output.text(", ");
                match mask.as_ref() {
                    ResourceIr::Number(mask) => {
                        output.text(format!("\"{mask}\""));
                    }
                    ResourceIr::String(mask) => {
                        output.text(mask.to_string());
                    }
                    mask => mask.emit_csharp(output, root_resource),
                }
                output.text(")");
            }
        }
    }
}

impl CsharpEmitter for OutputInstruction {
    fn emit_csharp(&self, output: &CodeBuffer) {
        let var_name = &self.name;

        if let Some(cond) = &self.condition {
            output.line(format!("{var_name} = {}", camel_case(cond)));
            output.text(format!("{INDENT}? "));
            let indented = output.indent(INDENT);
            self.value.emit_csharp(&indented, None);
            output.line(format!("\n{INDENT}: null;"));
        } else {
            output.text(format!("{var_name} = "));
            self.value.emit_csharp(output, None);
            output.line(";")
        }

        // Create CfnOutputs if the output is an export
        if let Some(export) = &self.export {
            if let Some(cond) = &self.condition {
                let indented = output.indent_with_options(IndentOptions {
                    indent: INDENT,
                    leading: Some(format!("if ({}) {{", camel_case(cond)).into()),
                    trailing: Some("}".into()),
                    trailing_newline: true,
                });
                self.emit_cfn_output(&indented, export, var_name);
            } else {
                self.emit_cfn_output(output, export, var_name);
            }
        }
    }
}

impl OutputInstruction {
    fn emit_cfn_output(&self, output: &CodeBuffer, export: &ResourceIr, var_name: &str) {
        let output = output.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some(
                format!(
                    "new CfnOutput(this, \"{}\", new CfnOutputProps {{",
                    &self.name
                )
                .into(),
            ),
            trailing: Some("});".into()),
            trailing_newline: true,
        });

        if let Some(description) = &self.description {
            output.line(format!("Description = \"{}\",", description.escape_debug()));
        }
        output.text("ExportName = ");
        export.emit_csharp(&output, None);
        output.text(",\n");
        output.line(format!("Value = {var_name} as string,"));
    }
}
#[cfg(test)]
mod tests {}
