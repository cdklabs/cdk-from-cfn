use super::Synthesizer;
use crate::code::{CodeBuffer, IndentOptions};
use crate::ir::conditions::ConditionIr;
use crate::ir::importer::ImportInstruction;
use crate::ir::outputs::OutputInstruction;
use crate::ir::reference::{Origin, PseudoParameter, Reference};
use crate::ir::resources::ResourceIr;
use crate::ir::CloudformationProgramIr;
use crate::parser::lookup_table::MappingInnerValue;
use crate::specification::{CfnType, Structure};
use std::borrow::Cow;
use std::io;
use std::rc::Rc;
use voca_rs::case::camel_case;

const INDENT: Cow<'static, str> = Cow::Borrowed("  ");
const STACK_NAME: Cow<'static, str> = Cow::Borrowed("NoctStack");

macro_rules! fill {
    ($code:ident; $leading:expr; $($lines:expr),* ; $trailing:expr) => {
        {
            let _class = $code.indent_with_options(IndentOptions {
                indent: INDENT,
                leading: Some($leading.into()),
                trailing: Some($trailing.into()),
                trailing_newline: true,
            });

            $(_class.line(format!($lines));)*
        }
    };
}

macro_rules! br {
    ($prefix: expr, $str:expr) => {
        format!("{}\n{INDENT}{}", $prefix, $str)
    };
}

pub struct Java {
    package_name: String,
}

impl Java {
    pub fn new(package_name: impl Into<String>) -> Self {
        Self {
            package_name: package_name.into(),
        }
    }

    //noinspection ALL
    fn write_header(&self, code: &CodeBuffer) {
        code.line(format!("package {};", self.package_name));
        code.newline();

        // base imports
        code.newline();
        code.line("import software.constructs.Construct;");
        code.newline();
        code.line("import java.util.*;");
        code.line("import java.util.stream.Collectors;");
        code.line("import software.amazon.awscdk.*;");
        code.line("import software.amazon.awscdk.App;");
        code.line("import software.amazon.awscdk.CfnMapping;");
        code.line("import software.amazon.awscdk.CfnTag;");
        code.line("import software.amazon.awscdk.Stack;");
        code.line("import software.amazon.awscdk.StackProps;");
        code.newline();
    }

    fn write_app(&self, writer: &CodeBuffer, description: &Option<String>) {
        let app_name = "NoctApp";
        let class = &writer.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some(format!("public class {} {{", app_name).into()),
            trailing: Some("}".into()),
            trailing_newline: true,
        });
        let main = &class.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some("public static void main(final String[] args) {".into()),
            trailing: Some("}".into()),
            trailing_newline: true,
        });
        main.line(format!("App app = new App();"));
        let stack_prop = main.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some("StackProps props = StackProps.builder()".into()),
            trailing: Some(format!("{INDENT}.build();").into()),
            trailing_newline: true,
        });
        match description {
            Some(desc) => stack_prop.line(format!(
                ".description(\"{}\")",
                desc.replace("\n", "\" + \n  \"")
            )),
            None => stack_prop.line("\"\""),
        };
        main.line(format!(
            "new {}(app, \"MyProjectStack\", props);",
            STACK_NAME
        ));
        main.line("app.synth();");
    }

    fn write_helpers(&self, code: &CodeBuffer) {
        const UTILS: &str = "class GenericList<T> extends LinkedList<T> {
  public GenericList<T> extend(final T object) {
    this.addLast(object);
    return this;
  }

  public GenericList<T> extend(final List<T> collection) {
    this.addAll(collection);
    return this;
  }
}

class GenericMap<T, S> extends HashMap<T, S> {
  public GenericMap<T, S> extend(final T key, final S value) {
    this.put(key, value);
    return this;
  }

  public List<CfnTag> getTags() {
    final List<CfnTag> tags = new LinkedList<>();
    for (Map.Entry<T, S> entry : this.entrySet()) {
      tags.add(
          CfnTag.builder()
              .key(String.valueOf(entry.getKey()))
              .value(String.valueOf(entry.getValue()))
              .build());
    }
    return tags;
  }
}

class Mapping<T> {
  private final String name;
  private final Construct scope;
  private final Map<String, Map<String, T>> inner = new TreeMap<>();

  public Mapping(Construct scope, String name) {
    this.name = name;
    this.scope = scope;
  }

  public Mapping<T> put(String primaryKey, String secondaryKey, T value) {
    final Map<String, T> map = inner.getOrDefault(primaryKey, new TreeMap<>());
    map.put(secondaryKey, value);
    inner.put(primaryKey, map);
    return this;
  }

  public CfnMapping get() {
    return CfnMapping.Builder.create(this.scope, this.name).mapping(this.inner).build();
  }
}
";
        code.line(UTILS);
    }

    fn write_mappings(ir: &CloudformationProgramIr, map: &Rc<CodeBuffer>) {
        map.line("// Start Mapping section");
        for mapping in &ir.mappings {
            let mut mapping_init = false;
            let map_name = name(&mapping.name);

            for (outer_key, inner) in mapping.map.iter() {
                let values: Vec<&MappingInnerValue> = inner.values().collect();
                let inner_type: &str = check_type(values);

                for (inner_key, value) in inner.iter() {
                    if !mapping_init {
                        map.line(format!(
                            "final Mapping<{inner_type}> {map_name} = new Mapping<>(this, \"{}\");",
                            &mapping.name
                        ));
                        mapping_init = true;
                    }
                    map.text(format!("{map_name}.put(\"{outer_key}\", \"{inner_key}\", "));

                    match value {
                        MappingInnerValue::Bool(bool) => {
                            map.text(format!("{}", if *bool { "true" } else { "false" }))
                        }
                        MappingInnerValue::Number(num) => map.text(format!("{num}")),
                        MappingInnerValue::Float(num) => map.text(format!("{num}")),
                        MappingInnerValue::String(str) => map.text(format!("{str:?}")),
                        MappingInnerValue::List(items) => {
                            let list = map.indent_with_options(IndentOptions {
                                indent: INDENT,
                                leading: None,
                                trailing: None,
                                trailing_newline: false,
                            });
                            list.text(format!("new GenericList<String>()"));
                            for item in items {
                                list.text(br!("", format!(".extend({item:?})")));
                            }
                        }
                    }
                    map.line(");")
                }
            }
            map.line(format!(
                "final CfnMapping {map_name}CfnMapping = {map_name}.get();",
            ));
            map.newline();
        }
    }

    fn write_parameters(ir: &CloudformationProgramIr, writer: &Rc<CodeBuffer>) {
        for input in &ir.constructor.inputs {
            let name = camel_case(&input.name);
            writer.line(format!(
                "CfnParameter {name} = CfnParameter.Builder.create(this, \"{}\")",
                &input.name
            ));
            match &input.description {
                Some(descr) => writer
                    .indent(INDENT)
                    .line(format!(".description(\"{}\")", descr)),
                None => {}
            };
            match &input.default_value {
                Some(val) => writer.indent(INDENT).line(format!(
                    ".defaultValue({}.valueOf(\"{}\"))",
                    &input.constructor_type, val
                )),
                None => {}
            };
            writer.line(format!("{INDENT}.build();"))
        }
    }

    fn write_resources(ir: &CloudformationProgramIr, writer: &Rc<CodeBuffer>) {
        for resource in &ir.resources {
            let class = resource.resource_type.type_name();
            let res_name = &resource.name;
            writer.newline();
            let res_info = writer.indent_with_options(IndentOptions {
                indent: INDENT,
                leading: Some(
                    format!(
                        "Cfn{class} {} = Cfn{class}.Builder.create(this, \"{res_name}\")",
                        name(&res_name)
                    )
                    .into(),
                ),
                trailing: Some(format!("{INDENT}.build();").into()),
                trailing_newline: true,
            });
            let properties = res_info.indent_with_options(IndentOptions {
                indent: INDENT,
                leading: None,
                trailing: None,
                trailing_newline: false,
            });
            for (key, value) in &resource.properties {
                let property = camel_case(key.as_str());
                let value = emit_java(value.clone(), &res_info, None);
                properties.line(format!(".{property}({value})"));
            }
            writer.newline();
        }
    }

    fn write_methods(class: Rc<CodeBuffer>) {
        class.newline();

        let static_helper = class.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some("public static <T> List<String> get(final List<T> input) {".into()),
            trailing: Some("}".into()),
            trailing_newline: true,
        });
        static_helper
            .line("return input.stream().map(String::valueOf).collect(Collectors.toList());");
    }

    fn write_conditions(ir: &CloudformationProgramIr, writer: &Rc<CodeBuffer>) {
        for condition in &ir.conditions {
            let name = &*condition.name;
            let val = &condition.value;
            writer.line(
                format!("CfnCondition {} = CfnCondition.Builder.create(this, \"{}\").expression({}).build();",
                        camel_case(name), name, emit_conditions(val.clone()))
            );
        }
    }

    fn write_outputs(ir: &CloudformationProgramIr, writer: Rc<CodeBuffer>) {
        let output_def = writer.clone();
        for output in &ir.outputs {
            emit_output(output, &output_def);
        }
    }
}

fn get_type(value: &MappingInnerValue) -> &str {
    let inner_type = match value {
        MappingInnerValue::Bool(_) => "Boolean",
        MappingInnerValue::Number(_) => "Integer",
        MappingInnerValue::Float(_) => "Double",
        MappingInnerValue::String(_) => "String",
        MappingInnerValue::List(_) => "List<String>",
    };
    inner_type
}

fn check_type(values: Vec<&MappingInnerValue>) -> &str {
    let mut found_type = "Object";
    let mut current_type;
    for (index, value) in values.iter().enumerate() {
        current_type = get_type(value);
        if index < 1 {
            found_type = current_type;
        }
        if !current_type.eq(found_type) {
            return "Object";
        }
    }
    return found_type;
}

impl Default for Java {
    fn default() -> Self {
        Self::new("com.acme.test.simple")
    }
}

impl Synthesizer for Java {
    fn synthesize(&self, ir: CloudformationProgramIr, into: &mut dyn io::Write) -> io::Result<()> {
        let code = CodeBuffer::default();

        self.write_header(&code);

        for import in &ir.imports {
            code.line(import.to_java());
        }
        code.newline();

        self.write_app(&code, &ir.description);

        fill!(code; format!("interface {}Props extends StackProps {{", STACK_NAME);; "}" );

        let class = code.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some(format!("class {} extends Stack {{", STACK_NAME).into()),
            trailing: Some("}".into()),
            trailing_newline: true,
        });

        fill!(class;
            format!("public {}(final Construct scope, final String id) {{", STACK_NAME);
            "super(scope, id, null);";
            "}" );

        let writer = class.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some(
                format!(
                    "public {}(final Construct scope, final String id, final StackProps props) {{",
                    STACK_NAME
                )
                .into(),
            ),
            trailing: Some("}".into()),
            trailing_newline: true,
        });
        writer.line("super(scope, id, props);");

        Self::write_mappings(&ir, &writer.clone());
        Self::write_parameters(&ir, &writer);
        Self::write_conditions(&ir, &writer);
        Self::write_resources(&ir, &writer);
        Self::write_outputs(&ir, writer);

        Self::write_methods(class);
        self.write_helpers(&code);

        code.write(into)
    }
}

impl ImportInstruction {
    fn to_java(&self) -> String {
        let mut parts: Vec<Cow<str>> = vec![match self.path[0].as_str() {
            "aws-cdk-lib" => "software.amazon.awscdk.services".into(),
            other => other.into(),
        }];
        parts.extend(self.path[1..].iter().map(|item| {
            item.chars()
                .filter(|ch| ch.is_alphanumeric())
                .collect::<String>()
                .into()
        }));

        let module = parts
            .iter()
            .take(parts.len() - 1)
            .map(|part| part.to_string())
            .collect::<Vec<_>>()
            .join(".");
        if !module.is_empty() {
            format!(
                "import {module}.{name}.*;",
                module = module,
                name = self.name,
            )
        } else {
            "".to_string()
        }
    }
}

fn match_cfn_type(input: &CfnType) -> String {
    String::from(match input {
        CfnType::Boolean => "Boolean",
        CfnType::Double => "Double",
        CfnType::Integer => "Integer",
        CfnType::Long => "Long",
        CfnType::Json => "JsonNode jsonNode = objectMapper.readTree(jsonString);",
        CfnType::String => "String",
        CfnType::Timestamp => "/*TODO*/",
    })
}

fn emit_conditions(condition: ConditionIr) -> String {
    match condition {
        ConditionIr::Ref(reference) => emit_reference(reference),
        ConditionIr::Str(str) => format!("{str:?}"),
        ConditionIr::Condition(x) => camel_case(&*x),
        ConditionIr::And(list) => {
            format!("Fn.conditionAnd({:?})", get_condition(list))
        }
        ConditionIr::Or(list) => {
            format!("Fn.conditionOr({:?})", get_condition(list))
        }
        ConditionIr::Not(cond) => {
            format!("Fn.conditionOr({:?})", emit_conditions(*cond))
        }
        ConditionIr::Equals(lhs, rhs) => {
            format!(
                "Fn.conditionEquals({}, {})",
                emit_conditions(*lhs),
                emit_conditions(*rhs)
            )
        }
        ConditionIr::Map(_, tlk, slk) => {
            format!(
                "Fn.map({}, {})",
                emit_conditions(*tlk),
                emit_conditions(*slk)
            )
        }
        ConditionIr::Split(sep, str) => {
            format!("Fn.split({sep:?}, {})", emit_conditions(*str))
        }
        ConditionIr::Select(index, str) => {
            format!("Fn.select({index:?}, get({}))", emit_conditions(*str))
        }
    }
}

fn emit_reference(reference: Reference) -> String {
    let origin = reference.origin;
    let name = reference.name;
    match origin {
        Origin::LogicalId { .. } => format!("\"{name}\""),
        Origin::GetAttribute { attribute, .. } => format!("Fn.getAtt(\"{name}\", \"{attribute}\")"),
        Origin::PseudoParameter(param) => get_pseudo_param(param),
        Origin::Parameter => format!("{}", camel_case(&*name)),
        Origin::Condition => name,
    }
}

fn get_pseudo_param(param: PseudoParameter) -> String {
    match param {
        PseudoParameter::Partition => "this.getPartition()",
        PseudoParameter::Region => "this.getRegion()",
        PseudoParameter::StackId => "this.getStackId()",
        PseudoParameter::StackName => "this.getStackName()",
        PseudoParameter::URLSuffix => "this.getUrlSuffix()",
        PseudoParameter::AccountId => "this.getAccount()",
        PseudoParameter::NotificationArns => "this.getNotificationArns()",
    }
    .into()
}

fn get_condition(list: Vec<ConditionIr>) -> String {
    let mut res = format!("");
    for (idx, cond) in list.iter().enumerate() {
        if idx == list.len() {
            res = format!("{res} {}", emit_conditions(cond.clone()))
        } else {
            res = format!("{res} {},", emit_conditions(cond.clone()))
        }
    }
    res
}

fn emit_output(output: &OutputInstruction, writer: &CodeBuffer) {
    let indented = writer.indent_with_options(IndentOptions {
        indent: INDENT,
        leading: Some(format!("CfnOutput.Builder.create(this, \"{}\")", output.name).into()),
        trailing: Some(format!("{INDENT}.build();").into()),
        trailing_newline: true,
    });
    let val = output.value.clone();
    indented.line(format!(
        ".value(String.valueOf({}))",
        emit_java(val, &*indented, None)
    ));

    let exp = &output.export;
    if let Some(value) = exp {
        // Value exists, use it
        indented.line(format!(
            ".exportName({})",
            emit_java(value.clone(), &*indented, None)
        ));
    }

    let description = &output.description;
    if let Some(value) = description {
        indented.line(format!(".description(\"{value}\")"));
    }

    let condition = &output.condition;
    if let Some(value) = condition {
        indented.line(format!(
            ".condition(CfnCondition.Builder.create(this, \"{}\").expression({}).build())",
            &output.name,
            camel_case(value).replace("\"", "")
        ));
    }
}

fn emit_java(this: ResourceIr, writer: &CodeBuffer, trailer: Option<&str>) -> String {
    match this {
        // Base cases
        ResourceIr::Null => "null".to_string(),
        ResourceIr::Bool(bool) => bool.to_string(),
        ResourceIr::Number(number) => format!("{number}"),
        ResourceIr::Double(number) => format!("{number}"),
        ResourceIr::String(text) => {
            if text.is_empty() {
                format!("/* validate FIXME */ \"\"")
            } else {
                format!("\"{text}\"")
            }
        }
        ResourceIr::ImportValue(text) => format!("\"{text}\""),

        ResourceIr::Object(structure, index_map) => match structure {
            Structure::Composite(_) => {
                let mut res = format!("new GenericMap<String, Object>()");
                for (key, value) in &index_map {
                    let element = emit_java((*value).clone(), writer, None);
                    if key.eq_ignore_ascii_case("Key") {
                        res = br!(res, format!(".extend({}", element))
                    }
                    if key.eq_ignore_ascii_case("Value") {
                        res = format!("{res},{})", element)
                    }
                }
                br!(res, ".getTags()")
            }

            Structure::Simple(cfn_type) => {
                let mut res = format!("new GenericMap<String, {}>()", match_cfn_type(&cfn_type));
                for (key, value) in &index_map {
                    let element = emit_java((*value).clone(), writer, None);
                    res = br!(res, format!(".extend({}, {})", key, element));
                }
                res
            }
        },

        ResourceIr::Array(structure, vect) => {
            let mut res: String;
            match structure {
                Structure::Composite(_) => {
                    res = format!("new GenericList<CfnTag>()");
                }

                Structure::Simple(cfn_type) => {
                    let current_type = match_cfn_type;
                    res = format!("new GenericList<{}>()", current_type(&cfn_type));
                }
            }
            for res_ir in vect {
                let element = emit_java(res_ir.clone(), writer, trailer);
                if !element.is_empty() {
                    res = br!(res, format!(".extend({})", element));
                }
            }
            res
        }

        ResourceIr::If(cond_id, val_true, val_false) => {
            format!(
                "Fn.conditionIf(\"{}\", {}, {})",
                cond_id,
                emit_java(*val_true, writer, None),
                emit_java(*val_false, writer, None)
            )
        }
        ResourceIr::Ref(reference) => emit_reference(reference),
        ResourceIr::Join(delimiter, resources) => {
            let mut res = format!("Fn.join(\"{delimiter}\", new GenericList<String>()");
            for resource in resources {
                let element = emit_java(resource, writer, None);
                if !element.is_empty() {
                    res = br!(res, format!(".extend({})", element))
                }
            }
            format!("{res})")
        }
        ResourceIr::Split(string, resource) => {
            format!(
                "Fn.split({}, String.valueOf({}))",
                string,
                emit_java(*resource, writer, None)
            )
        }
        ResourceIr::Base64(resource) => {
            format!(
                "Fn.base64(String.valueOf({}))",
                emit_java(*resource, writer, None)
            )
        }
        ResourceIr::GetAZs(resource) => {
            format!(
                "Fn.getAzs(String.valueOf({}))",
                emit_java(*resource, writer, None)
            )
        }
        ResourceIr::Sub(resources) => {
            if let Some((first_elem, vect)) = resources.split_first() {
                let body = emit_java(first_elem.clone(), writer, None);
                if vect.is_empty() {
                    format!("Fn.sub(String.valueOf({}))", body);
                }

                let mut res = format!(
                    "Fn.sub(String.valueOf({}), new GenericMap<String, String>()",
                    body
                );
                for chunk in vect.chunks(2) {
                    if let [key, value] = chunk {
                        let key_element = emit_java(key.clone(), writer, None);
                        let value_element = emit_java(value.clone(), writer, None);
                        res = br!(res, format!(".extend({}, {})", key_element, value_element));
                    }
                }
                return format!("{res})");
            }
            panic!("🚨 Fn::Sub improperly formatted")
        }
        ResourceIr::Map(resource, key, value) => {
            format!(
                "Fn.findInMap(\"{}\", {}, {})",
                resource,
                emit_java(*key, writer, None),
                emit_java(*value, writer, None),
            )
        }
        ResourceIr::Cidr(p0, p1, p2) => {
            format!(
                "Fn.cidr(String.valueOf({}), {}, String.valueOf({}))",
                emit_java(*p0, writer, None),
                emit_java(*p1, writer, None),
                emit_java(*p2, writer, None)
            )
        }
        ResourceIr::Select(size, resource) => {
            let used_type: String = match *resource.clone() {
                ResourceIr::Array(structure, _) => match structure {
                    Structure::Simple(cfn_type) => match_cfn_type(&cfn_type),
                    _ => "".into(),
                },
                _ => "".into(),
            };
            if !used_type.is_empty() {
                format!(
                    "{}.valueOf(Fn.select({},get({})))",
                    used_type,
                    size,
                    emit_java(*resource, writer, None)
                )
            } else {
                format!(
                    "Fn.select({},get({}))",
                    size,
                    emit_java(*resource, writer, None)
                )
            }
        }
    }
}

fn name(key: &String) -> String {
    camel_case(&key)
        .chars()
        .filter(|c| c.is_alphanumeric())
        .collect()
}

#[cfg(test)]
mod tests {}
