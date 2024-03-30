use crate::cdk::{ItemType, Primitive, Schema, TypeReference};
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
use crate::Error;
use std::borrow::Cow;
use std::io;
use voca_rs::case::{camel_case, pascal_case};

use super::Synthesizer;

const INDENT: Cow<'static, str> = Cow::Borrowed("    ");

pub struct CSharp<'a> {
    schema: &'a Schema,
}

impl<'a> CSharp<'a> {
    pub fn new(schema: &'a Schema) -> Self {
        Self { schema }
    }
}

impl Default for CSharp<'_> {
    fn default() -> Self {
        Self::new(Schema::builtin())
    }
}

impl Synthesizer for CSharp<'_> {
    fn synthesize(
        &self,
        ir: CloudformationProgramIr,
        into: &mut dyn io::Write,
        stack_name: &str,
    ) -> Result<(), Error> {
        // Initialize the code buffer in which all of the code will be generated
        let code = CodeBuffer::default();

        // Imports
        for import in &ir.imports {
            code.line(import.to_csharp()?)
        }
        code.line("using Constructs;");
        code.line("using System.Collections.Generic;");
        code.newline();

        // Namespace definition
        let namespace = code.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some(format!("namespace {}\n{{", stack_name).into()),
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
            ctor.line(format!("props ??= new {stack_name}Props();"));
            for param in have_default_or_special_type_params {
                let name = pascal_case(&param.name);
                // example: AWS::EC2::Image::Id, List<AWS::EC2::VPC::Id>, AWS::SSM::Parameter::Value<List<String>>
                if param.constructor_type.contains("AWS::")
                    || param.no_echo.as_ref().is_some_and(|x| x == "true")
                {
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
                    let list_optional_prefix = match &param.constructor_type {
                        t if t.contains("List") => "string.Join(\",\", ",
                        _ => "",
                    };
                    let list_optional_suffix = match &param.constructor_type {
                        t if t.contains("List") => ")",
                        _ => "",
                    };
                    if let Some(v) = &param.default_value {
                        cfn_param.line(format!(
                            "Default = {list_optional_prefix}props.{name}{list_optional_suffix} ?? \"{}\",",
                            v.escape_debug()
                        ));
                    } else {
                        cfn_param.line(format!(
                            "Default = {list_optional_prefix}props.{name}{list_optional_suffix},"
                        ));
                    };
                    if let Some(v) = &param.description {
                        cfn_param.line(format!("Description = \"{}\",", v));
                    };
                    if let Some(v) = &param.no_echo {
                        cfn_param.line(format!("NoEcho = {v},"));
                    }
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
                                "Boolean" => value.clone(),
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

        // Transforms
        if !ir.transforms.is_empty() {
            ctor.line("// Transforms");
            for transform in &ir.transforms {
                ctor.line(format!("AddTransform(\"{transform}\");"));
            }
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
                map.text(format!(
                    "[\"{key}\"] = new Dictionary<string, {leaf_type}> {{"
                ));
                for (inner_key, inner_value) in inner {
                    match inner_value {
                        MappingInnerValue::Bool(_)
                        | MappingInnerValue::Float(_)
                        | MappingInnerValue::Number(_) => {
                            map.text(format!("[\"{inner_key}\"] = {inner_value}, "));
                        }
                        MappingInnerValue::String(s) => {
                            map.text(format!("[\"{inner_key}\"] = \"{s}\", "));
                        }
                        MappingInnerValue::List(l) => {
                            map.text(format!("[\"{inner_key}\"] = new string[] {{"));
                            for list_item in l {
                                map.text(format!("\"{list_item}\", "));
                            }
                            map.text("}, ");
                        }
                    }
                }
                map.line("},");
            }
        }

        // Conditions
        if !ir.conditions.is_empty() {
            ctor.newline();
            ctor.line("// Conditions");
        }
        for condition in &ir.conditions {
            ctor.text(format!("bool {} = ", camel_case(&condition.name)));
            condition.value.emit_csharp(&ctor, self.schema)?;
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
                resource_constructor.text(format!("{name} = ", name = pascal_case(name)));
                value.emit_csharp(&resource_constructor, self.schema)?;
                resource_constructor.text(",");
                resource_constructor.newline();
            }
        }

        // Set values for the outputs
        if !ir.outputs.is_empty() {
            ctor.newline();
            ctor.line("// Outputs");

            for op in &ir.outputs {
                op.emit_csharp(&ctor, self.schema)?;
            }
        }

        Ok(code.write(into)?)
    }
}

impl ImportInstruction {
    fn to_csharp(&self) -> Result<String, Error> {
        let mut parts: Vec<String> = vec!["Amazon".to_string(), "CDK".to_string()];
        match self.organization.as_str() {
            "AWS" => {
                match &self.service {
                    Some(service) => {
                        parts.push("AWS".to_string());
                        parts.push(service.into());
                    }
                    None => {}
                };
            }
            "Alexa" => {
                parts.push("Alexa".to_string());
                parts.push(pascal_case(self.service.as_ref().unwrap()));
            }
            org => {
                return Err(Error::ImportInstructionError {
                    message: format!("Expected organization to be AWS or Alexa. Found {org}"),
                })
            }
        };
        let namespace = parts.join(".");

        Ok(format!("using {namespace};"))
    }
}

impl ConstructorParameter {
    fn to_csharp_auto_property(&self) -> String {
        let prop_type = match &self.constructor_type {
            t if t.contains("List") => "string[]",
            t if t == "Boolean" => "bool?",
            _ => "string",
        };

        format!(
            "public {prop_type} {} {{ get; set; }}",
            pascal_case(&self.name)
        )
    }
}

trait CsharpEmitter {
    fn emit_csharp(&self, output: &CodeBuffer, schema: &Schema) -> Result<(), Error>;
}

impl CsharpEmitter for ConditionIr {
    fn emit_csharp(&self, output: &CodeBuffer, _schema: &Schema) -> Result<(), Error> {
        match self {
            ConditionIr::Ref(reference) => {
                reference.emit_csharp(output);
                Ok(())
            }
            ConditionIr::Str(str) => Ok(output.text(format!("\"{str}\""))),
            ConditionIr::Condition(condition) => {
                output.text(camel_case(condition));
                Ok(())
            }

            ConditionIr::And(list) => {
                for (index, condition) in list.iter().enumerate() {
                    if index > 0 {
                        output.text(" && ");
                    }
                    condition.emit_csharp(output, _schema)?;
                }
                Ok(())
            }
            ConditionIr::Or(list) => {
                for (index, condition) in list.iter().enumerate() {
                    if index > 0 {
                        output.text(" || ");
                    }
                    condition.emit_csharp(output, _schema)?;
                }
                Ok(())
            }

            ConditionIr::Not(condition) => {
                output.text("!(");
                condition.emit_csharp(output, _schema)?;
                output.text(")");
                Ok(())
            }

            ConditionIr::Equals(left, right) => {
                left.emit_csharp(output, _schema)?;
                output.text(" == ");
                right.emit_csharp(output, _schema)?;
                Ok(())
            }

            ConditionIr::Map(map, top_level_key, second_level_key) => {
                output.text(camel_case(map));
                output.text("[");
                top_level_key.emit_csharp(output, _schema)?;
                output.text("][");
                second_level_key.emit_csharp(output, _schema)?;
                output.text("]");
                Ok(())
            }
            ConditionIr::Split(sep, str) => match str.as_ref() {
                ConditionIr::Str(str) => {
                    output.text(format!("'{str}'", str = str.escape_debug()));
                    output.text(format!(".Split('{sep}')", sep = sep.escape_debug()));
                    Ok(())
                }
                other => {
                    output.text(format!("Fn.Split(\"{sep}\", "));
                    other.emit_csharp(output, _schema)?;
                    output.text(")");
                    Ok(())
                }
            },
            ConditionIr::Select(index, str) => {
                output.text(format!("Fn.Select({index}, "));
                str.emit_csharp(output, _schema)?;
                output.text(")");
                Ok(())
            }
        }
    }
}

impl Reference {
    fn emit_csharp(&self, output: &CodeBuffer) {
        match &self.origin {
            Origin::Condition => output.text(camel_case(&self.name)),
            Origin::GetAttribute {
                attribute,
                conditional: _,
            } => output.text(format!(
                "{}.Attr{}",
                camel_case(&self.name),
                attribute.replace('.', "")
            )),
            Origin::LogicalId { conditional: _ } => {
                output.text(format!("{}.Ref", camel_case(&self.name.replace('.', ""))))
            }
            Origin::CfnParameter | Origin::Parameter => {
                output.text(format!("props.{}", pascal_case(&self.name)))
            }
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
    fn emit_csharp(&self, output: &CodeBuffer, schema: &Schema) -> Result<(), Error> {
        match self {
            ResourceIr::Null => {
                output.text("null");
                Ok(())
            }
            ResourceIr::Bool(bool) => {
                output.text(bool.to_string());
                Ok(())
            }
            ResourceIr::Number(number) => {
                output.text(number.to_string());
                Ok(())
            }
            ResourceIr::Double(double) => {
                output.text(double.to_string());
                Ok(())
            }
            ResourceIr::String(str) => {
                if str.lines().count() > 1 {
                    output.text(format!("@\"{str}\""));
                } else {
                    output.text(format!("\"{str}\""));
                };
                Ok(())
            }
            ResourceIr::Array(_structure, array) => {
                let array_block = output.indent_with_options(IndentOptions {
                    indent: INDENT,
                    leading: Some("new []\n{".into()),
                    trailing: Some("}".into()),
                    trailing_newline: false,
                });
                for item in array {
                    item.emit_csharp(&array_block, schema)?;
                    array_block.text(",");
                    array_block.newline();
                }
                Ok(())
            }
            ResourceIr::Object(structure, properties) => match &structure {
                TypeReference::Named(name)
                | TypeReference::List(ItemType::Static(TypeReference::Named(name))) => {
                    match name.as_ref() {
                        "CfnTag" => {
                            let object_block = output.indent_with_options(IndentOptions {
                                indent: INDENT,
                                leading: Some("new CfnTag\n{".into()),
                                trailing: Some("}".into()),
                                trailing_newline: false,
                            });
                            for (name, val) in properties {
                                object_block.text(format!("{name} = "));
                                val.emit_csharp(&object_block, schema)?;
                                object_block.text(",");
                                object_block.newline();
                            }
                            Ok(())
                        }
                        name => {
                            let name = &schema.type_named(name).unwrap().name.csharp;
                            let object_block = output.indent_with_options(IndentOptions {
                                indent: INDENT,
                                leading: Some(format!("new {}\n{{", name.name).into()),
                                trailing: Some("}".into()),
                                trailing_newline: false,
                            });
                            for (name, val) in properties {
                                object_block.text(format!("{name} = "));
                                val.emit_csharp(&object_block, schema)?;
                                object_block.text(",");
                                object_block.newline();
                            }
                            Ok(())
                        }
                    }
                }
                TypeReference::Primitive(Primitive::Json) => {
                    let object_block = output.indent_with_options(IndentOptions {
                        indent: INDENT,
                        leading: Some("new Dictionary<string, object>\n{".into()),
                        trailing: Some("}".into()),
                        trailing_newline: false,
                    });
                    for (name, val) in properties {
                        object_block.text(format!("{{ \"{name}\", "));
                        val.emit_csharp(&object_block, schema)?;
                        object_block.text("},");
                        object_block.newline();
                    }
                    Ok(())
                }
                TypeReference::Map(_) => {
                    let object_block = output.indent_with_options(IndentOptions {
                        indent: INDENT,
                        leading: Some("new Dictionary<string, string>\n{".into()),
                        trailing: Some("}".into()),
                        trailing_newline: false,
                    });
                    for (name, val) in properties {
                        object_block.text(format!("{{ \"{name}\", "));
                        val.emit_csharp(&object_block, schema)?;
                        object_block.text("},");
                        object_block.newline();
                    }
                    Ok(())
                }
                other => {
                    Err(Error::TypeReferenceError {
                        message: format!(
                            "Type reference {other:#?} not implemented for ResourceIr::Object"
                        ),
                    })
                }
            },
            ResourceIr::If(cond, when_true, when_false) => {
                output.text(format!("{} ? ", camel_case(cond)));
                when_true.emit_csharp(output, schema)?;
                output.text(" : ");
                when_false.emit_csharp(output, schema)?;
                Ok(())
            }
            ResourceIr::Join(sep, list) => {
                let items = output.indent_with_options(IndentOptions {
                    indent: INDENT,
                    leading: Some(
                        format!(
                            "string.Join(\"{sep}\", new []\n{{",
                            sep = sep.escape_debug()
                        )
                        .into(),
                    ),
                    trailing: Some("})".into()),
                    trailing_newline: false,
                });
                for item in list {
                    item.emit_csharp(&items, schema)?;
                    items.text(",");
                    items.newline();
                }
                Ok(())
            }
            ResourceIr::Split(sep, str) => match str.as_ref() {
                ResourceIr::String(str) => {
                    output.text(format!("\"{str}\"", str = str.escape_debug()));
                    output.text(format!(".Split('{sep}')", sep = sep.escape_debug()));
                    Ok(())
                }
                other => {
                    output.text(format!("Fn.Split('{sep}', "));
                    other.emit_csharp(output, schema)?;
                    output.text(")");
                    Ok(())
                }
            },
            ResourceIr::Ref(reference) => {
                reference.emit_csharp(output);
                Ok(())
            }
            ResourceIr::Sub(parts) => {
                output.text("$\"");
                for part in parts {
                    match part {
                        ResourceIr::String(lit) => output.text(lit.clone()),
                        other => {
                            output.text("{");
                            other.emit_csharp(output, schema)?;
                            output.text("}");
                        }
                    }
                }
                output.text("\"");
                Ok(())
            }
            ResourceIr::Map(table, top_level_key, second_level_key) => {
                output.text(camel_case(table));
                output.text("[");
                top_level_key.emit_csharp(output, schema)?;
                output.text("][");
                second_level_key.emit_csharp(output, schema)?;
                output.text("]");
                Ok(())
            }
            ResourceIr::Base64(value) => {
                output.text("Fn.Base64(");
                value.emit_csharp(output, schema)?;
                output.text(" as string)");
                Ok(())
            }
            ResourceIr::ImportValue(import) => {
                output.text("Fn.ImportValue(");
                import.emit_csharp(output, schema)?;
                output.text(")");
                Ok(())
            }
            ResourceIr::GetAZs(region) => {
                output.text("Fn.GetAzs(");
                region.emit_csharp(output, schema)?;
                output.text(")");
                Ok(())
            }
            ResourceIr::Select(idx, list) => match list.as_ref() {
                ResourceIr::Array(_, array) => {
                    if *idx <= array.len() {
                        array[*idx].emit_csharp(output, schema)?;
                    } else {
                        output.text("null");
                    }
                    Ok(())
                }
                other => {
                    output.text(format!("Fn.Select({idx}, "));
                    other.emit_csharp(output, schema)?;
                    output.text(")");
                    Ok(())
                }
            },
            ResourceIr::Cidr(cidr_block, count, mask) => {
                output.text("Fn.Cidr(");
                cidr_block.emit_csharp(output, schema)?;
                output.text(", ");
                count.emit_csharp(output, schema)?;
                output.text(", ");
                match mask.as_ref() {
                    ResourceIr::Number(mask) => {
                        output.text(format!("\"{mask}\""));
                    }
                    ResourceIr::String(mask) => {
                        output.text(mask.to_string());
                    }
                    mask => mask.emit_csharp(output, schema)?,
                }
                output.text(")");
                Ok(())
            }
        }
    }
}

impl CsharpEmitter for OutputInstruction {
    fn emit_csharp(&self, output: &CodeBuffer, schema: &Schema) -> Result<(), Error> {
        let var_name = &self.name;

        if let Some(cond) = &self.condition {
            output.line(format!("{var_name} = {}", camel_case(cond)));
            output.text(format!("{INDENT}? "));
            let indented = output.indent(INDENT);
            self.value.emit_csharp(&indented, schema)?;
            output.line(format!("\n{INDENT}: null;"));
        } else {
            output.text(format!("{var_name} = "));
            self.value.emit_csharp(output, schema)?;
            output.line(";");
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
                self.emit_cfn_output(&indented, export, var_name, schema)?;
            } else {
                self.emit_cfn_output(output, export, var_name, schema)?;
            }
        }

        Ok(())
    }
}

impl OutputInstruction {
    fn emit_cfn_output(
        &self,
        output: &CodeBuffer,
        export: &ResourceIr,
        var_name: &str,
        schema: &Schema,
    ) -> Result<(), Error> {
        let output = output.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some(
                format!(
                    "new CfnOutput(this, \"CfnOutput{}\", new CfnOutputProps {{",
                    &self.name
                )
                .into(),
            ),
            trailing: Some("});".into()),
            trailing_newline: true,
        });

        output.line(format!("Key = \"{}\",", &self.name));
        if let Some(description) = &self.description {
            output.line(format!("Description = \"{}\",", description.escape_debug()));
        }
        output.text("ExportName = ");
        export.emit_csharp(&output, schema)?;
        output.text(",\n");
        output.line(format!("Value = {var_name} as string,"));

        Ok(())
    }
}

#[cfg(test)]
mod tests;
