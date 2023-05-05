use super::resource::ResourceValue;

#[derive(Clone, Debug, PartialEq, serde::Deserialize)]
#[serde(rename_all = "PascalCase")]
pub struct Output {
    pub value: ResourceValue,
    pub export: Option<ResourceValue>,
    pub condition: Option<String>,
    pub description: Option<String>,
}
