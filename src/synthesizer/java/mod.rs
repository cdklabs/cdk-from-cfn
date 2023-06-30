#![allow(unused_variables)]

use crate::code::{CodeBuffer, IndentOptions};
use crate::ir::CloudformationProgramIr;
use crate::ir::importer::ImportInstruction;
use crate::ir::resources::ResourceIr;
use crate::ir::conditions::ConditionIr;
use crate::parser::lookup_table::MappingInnerValue;
use crate::specification::{CfnType, Structure};
use std::any::{type_name};
use std::borrow::Cow;
use std::fmt::{Debug};
use std::io;
use std::rc::Rc;
use super::Synthesizer;
use voca_rs::case::camel_case;
use crate::ir::outputs::OutputInstruction;
use crate::ir::reference::{Origin, Reference};

const INDENT: Cow<'static, str> = Cow::Borrowed("\t");

macro_rules! fill {
    ($code:ident; $leading:expr; $($lines:expr),* ; $trailing:expr) => {
        {
            let class = $code.indent_with_options(IndentOptions {
                indent: INDENT,
                leading: Some($leading.into()),
                trailing: Some($trailing.into()),
                trailing_newline: true,
            });

            $(class.line(format!($lines));)*
        }
    };
}

fn debug<T: Debug>(value: T, prefix: Option<&str>) {
    let type_name = type_name::<T>();
    println!("[🔎] {:?}: ({type_name}) {:?}", prefix, value);
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
        code.line("import com.fasterxml.jackson.databind.JsonNode;");
        code.line("import com.fasterxml.jackson.databind.ObjectMapper;");
        code.newline();
        code.line("import software.constructs.Construct;");
        code.newline();
        code.line("import java.util.*;");
        code.line("import software.amazon.awscdk.*;");
        code.line("import software.amazon.awscdk.Fn.*;");
        code.line("import software.amazon.awscdk.CfnMapping;");
        code.line("import software.amazon.awscdk.CfnTag;");
        code.line("import software.amazon.awscdk.Stack;");
        code.line("import software.amazon.awscdk.StackProps;");
        code.newline();
    }

    fn write_helpers(&self, code: &CodeBuffer) {
        const UTILS: &str = "class GenericSet<T> {
    private final Set<T> set = new HashSet<>();

    public GenericSet<T> add(final T object) {
        this.set.add(object);
        return this;
    }

    public Set<T> get() {
        return this.set;
    }
}

class GenericList<T> {
    private final List<T> list = new LinkedList<>();

    public GenericList<T> add(final T object) {
        this.list.add(object);
        return this;
    }
    public List<T> get() {
        return this.list;
    }
}

class GenericMap<T, S> {
    private final Map<T, S> map = new HashMap<>();

    public GenericMap<T, S> add(final T key, final S value) {
        this.map.put(key, value);
        return this;
    }

    public Map<T, S> get() {
        return this.map;
    }

    public List<CfnTag> getTags() {
        final List<CfnTag> tags = new LinkedList<>();
        for(Map.Entry<T,S> entry : this.map.entrySet()) {
            tags.add(CfnTag.builder().key(String.valueOf(entry.getKey())).value(String.valueOf(entry.getValue())).build());
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
        map.line("{ // Start Mapping section");
        for mapping in &ir.mappings {
            let mut mapping_init = false;
            let map_name = name(&mapping.name);

            for (outer_key, inner) in mapping.map.iter() {
                let values: Vec<&MappingInnerValue> = inner.values().collect();
                let (mix_types, inner_type): (bool, &str) = check_type(values);

                for (inner_key, value) in inner.iter() {
                    if !mapping_init {
                        map.line(format!("final Mapping<{inner_type}> {map_name} = new Mapping<>(this, \"{}\");", &mapping.name));
                        mapping_init = true;
                    }
                    map.text(format!("{map_name}.put(\"{outer_key}\", \"{inner_key}\", "));

                    match value {
                        MappingInnerValue::Bool(bool) => {
                            map.text(format!("{}", if *bool { "true" } else { "false" }))
                        }
                        MappingInnerValue::Number(num) => {
                            map.text(format!("{num}"))
                        }
                        MappingInnerValue::Float(num) => {
                            map.text(format!("{num}"))
                        }
                        MappingInnerValue::String(str) => {
                            map.text(format!("{str:?}"))
                        }
                        MappingInnerValue::List(items) => {
                            let list = map.indent_with_options(IndentOptions {
                                indent: INDENT,
                                leading: Some(format!("new GenericList<String>()").into()),
                                trailing: Some("\n".into()),
                                trailing_newline: false,
                            });
                            for item in items {
                                list.text(format!(".add({item:?})"));
                            }
                            list.line(".get()");
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
        map.line("} // End Mapping section\n");
    }
}

fn get_type(value: &MappingInnerValue) -> &str {
    let inner_type = match value {
        MappingInnerValue::Bool(bool) => "Boolean",
        MappingInnerValue::Number(num) => "Integer",
        MappingInnerValue::Float(num) => "Double",
        MappingInnerValue::String(str) => "String",
        MappingInnerValue::List(items) => "List<String>",
    };
    inner_type
}

fn check_type(values: Vec<&MappingInnerValue>) -> (bool, &str) {
    let mut found_type = "Object";
    let mut current_type;
    for (index, value) in values.iter().enumerate() {
        current_type = get_type(value);
        if index < 1 {
            found_type = current_type;
        }
        if !current_type.eq(found_type) {
            return (false, "Object");
        }
    }
    return (true, found_type);
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

        fill!(code; "interface NoctStackProps extends StackProps {";; "}" );

        self.write_helpers(&code);

        let class = code.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some("public class NoctStack extends Stack {".into()),
            trailing: Some("}".into()),
            trailing_newline: true,
        });

        fill!(class;
            "public NoctStack(final Construct scope, final String id) {";
            "super(scope, id, null);";
            "}" );

        let ctor = class.indent_with_options(IndentOptions {
            indent: INDENT,
            leading: Some("public NoctStack(final Construct scope, final String id, final StackProps props) {".into()),
            trailing: Some("}".into()),
            trailing_newline: true,
        });
        ctor.line("super(scope, id, props);");

        Self::write_mappings(&ir, &ctor.clone());
        let resource_def = ctor.clone();
        for resource in &ir.resources {
            let class = resource.resource_type.type_name();
            let res_name = &resource.name;
            resource_def.newline();
            let params = resource_def.indent_with_options(IndentOptions {
                indent: INDENT,
                leading: Some(format!("Cfn{class} {} = Cfn{class}.Builder.create(this, \"{res_name}\")", name(&res_name)).into()),
                trailing: Some(".build();".into()),
                trailing_newline: true,
            });
            for (key, value) in &resource.properties {
                params.text(format!(".{}({})", camel_case(key.as_str()), emit_java(value.clone(), &params, None)));
            }
            resource_def.newline();
        }


        let condition_def = ctor.clone();
        for condition in &ir.conditions {
            let val = condition.value.clone();
            emit_conditions(val, &condition_def, None);
        }

        let output_def = ctor.clone();
        for output in &ir.outputs {
            emit_output(output, &output_def, None);
        }

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
        CfnType::Double | CfnType::Integer | CfnType::Long => "Double",
        CfnType::Json => "JsonNode jsonNode = objectMapper.readTree(jsonString);",
        CfnType::String => "String",
        CfnType::Timestamp => "/*TODO*/"
    })
}

fn emit_conditions(reference: ConditionIr, writer: &CodeBuffer, trailer: Option<&str>) {
    match reference {
        ConditionIr::Ref(reference) => {
            writer.text("Fn.ref(");
            emit_reference(reference, writer, None);
            writer.text(")");
        }
        ConditionIr::Str(str) => writer.text(format!("{str:?}")),
        ConditionIr::Condition(x) => writer.text(format!("\"{x:?}\"")),

        ConditionIr::And(list) => {
            writer.text("Fn.conditionAnd(");
            get_condition(writer, list);
            writer.text(")");
        }
        ConditionIr::Or(list) => {
            writer.text("Fn.conditionOr(");
            get_condition(writer, list);
            writer.text(")");
        }

        ConditionIr::Not(cond) => {
            writer.text("Fn.conditionNot(");
            emit_conditions(*cond, writer, None);
            writer.text(")");
        }

        ConditionIr::Equals(lhs, rhs) => {
            writer.text("Fn.conditionEquals(");
            emit_conditions(*lhs, writer, None);
            writer.text(", ");
            emit_conditions(*rhs, writer, None);
            writer.text(")");
        }

        ConditionIr::Map(map, tlk, slk) => {
            writer.text(format!("Fn.map({}, ", map));
            emit_conditions(*tlk, writer, None);
            writer.text(", ");
            emit_conditions(*slk, writer, None);
            writer.text(")");
        }
        ConditionIr::Split(sep, str) => {
            writer.text(format!("Fn.split({sep:?}), "));
            emit_conditions(*str, writer, None);
            writer.text(")");
        }
        ConditionIr::Select(index, str) => {
            writer.text(format!("Fn.select({index:?}, "));
            emit_conditions(*str, writer, None);
            writer.text(")");
        }
    }
    if let Some(trailer) = trailer {
        writer.text(trailer.to_owned())
    }
}

fn emit_reference(reference: Reference, writer: &CodeBuffer, trailer: Option<&str>) -> String {
    let origin = reference.origin;
    let name = reference.name;
    match origin {
        Origin::LogicalId { conditional } => format!("Fn.ref({name})"),
        Origin::GetAttribute { attribute, conditional } => format!("Fn.getAtt({attribute}, {name})"),
        Origin::Parameter {} => format!("Fn.getValueFromLookup({name})"),
        Origin::Condition => format!("new CfnCondition(this, {name})"),
        Origin::PseudoParameter(_) => format!("/* TODO pseudo-param {name}!*/")
    }
}

fn get_condition(output: &CodeBuffer, list: Vec<ConditionIr>) {
    for (idx, cond) in list.iter().enumerate() {
        if idx > 0 {
            output.text(", ");
        }
        emit_conditions(cond.clone(), output, None);
    }
}

fn emit_output(output: &OutputInstruction, writer: &CodeBuffer, trailer: Option<&str>) {
    let indented = writer.indent_with_options(IndentOptions {
        indent: INDENT,
        leading: Some(format!("CfnOutput.Builder.create(this, \"{}\")", output.name).into()),
        trailing: Some(format!(".build();").into()),
        trailing_newline: true,
    });
    let val = output.value.clone();
    indented.line(format!(".value(String.valueOf({}))", emit_java(val, &*indented, None)));

    let exp = &output.export;
    if let Some(value) = exp {
        // Value exists, use it
        indented.line(format!(".export(\"{}\")", emit_java(value.clone(), &*indented, None)));
    }

    let description = &output.description;
    if let Some(value) = description {
        indented.line(format!(".description(\"{value}\")"));
    }

    let condition = &output.condition;
    if let Some(value) = condition {
        indented.line(format!(".condition(\"{value}\")"));
    }
}

fn emit_java(this: ResourceIr, writer: &CodeBuffer, trailer: Option<&str>) -> String {
    debug(this.clone(), None);

    match this {
        // Base cases
        ResourceIr::Null => "null".to_string(),
        ResourceIr::Bool(bool) => bool.to_string(),
        ResourceIr::Number(number) => format!("{number}"),
        ResourceIr::Double(number) => format!("{number}"),
        ResourceIr::String(text) => format!("{text}"),
        ResourceIr::ImportValue(text) => format!("\"{text}\""),

        ResourceIr::Object(obj, indexmap) => {
            let mut res = format!("new GenericMap<String, Object>()");
            for (key, value) in &indexmap {
                res = format!("{res}\n.add({},{})", key, emit_java((*value).clone(), writer, None))
            }
            res
        }
        ResourceIr::Array(struc, vect) => {
            match struc {
                Structure::Simple(simple) => {
                    format!("{}", match_cfn_type(&simple))
                }
                Structure::Composite(com_struc) => {
                    if !com_struc.eq_ignore_ascii_case("Tag") {
                        panic!("/*🚨TODO composite structure, not tag!*/");
                    }

                    let mut res = format!("new GenericList<Object>()\n");
                    for element in vect.iter() {
                        res = format!("{res}\n{INDENT}.add({})", emit_java(element.clone(), writer, trailer));
                    }
                    return format!("{res}\n.getTags()\n");
                }
            }
        }

        ResourceIr::If(cond_id, val_true, val_false) => {
            format!("Fn.conditionIf(\"{}\", {}, {})", cond_id, emit_java(*val_true, writer, None), emit_java(*val_false, writer, None))
        }
        ResourceIr::Ref(reference) => {
            emit_reference(reference, writer, None)
        }
        ResourceIr::Join(delimiter, resources) => {
            let mut res = format!("Fn.join(\"{delimiter}\", new GenericList<String>()");
            for resource in resources {
                res = format!("{res}\n{INDENT}.add({})", emit_java(resource, writer, None))
            }
            format!("{res}\n{INDENT}.get()")
        }
        ResourceIr::Split(string, resource) => {
            format!("Fn.split({}, String.valueOf({})", string, emit_java(*resource, writer, None))
        }
        ResourceIr::Base64(resource) => {
            format!("Fn.base64(\"{}\")", emit_java(*resource, writer, None))
        }
        ResourceIr::GetAZs(resource) => {
            format!("Fn.getAz(\"{}\")", emit_java(*resource, writer, None))
        }
        ResourceIr::Sub(resources) => {
            if let Some((first_elem, vect)) = resources.split_first() {
                let mut res = format!("Fn.sub(\"{}\", ", emit_java(first_elem.clone(), writer, None));
                for resource in vect {
                    res = format!("{res}\n{}", emit_java(resource.clone(), writer, None));
                }
                return format!("{res})\n");
            }
            panic!("🚨 Fn::Sub improperly formatted")
        }
        ResourceIr::Map(resource, key, value) => {
            format!("/* TODO map */")
        }
        ResourceIr::Cidr(p0, p1, p2) => {
            format!("Fn.cidr(\"{}\", {}, String.valueOf({}))",
                    emit_java(*p0, writer, None),
                    emit_java(*p1, writer, None),
                    emit_java(*p2, writer, None)
            )
        }
        ResourceIr::Select(size, resource) => {
            format!("Fn.select({},{})", size, emit_java(*resource, writer, None))
        }
    }
}

fn name(key: &String) -> String {
    camel_case(&key).chars()
        .filter(|c| c.is_alphanumeric())
        .collect()
}

#[cfg(test)]
mod tests {}
