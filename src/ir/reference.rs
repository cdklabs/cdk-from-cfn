use voca_rs::case::{camel_case, pascal_case};

#[derive(Debug, Clone, PartialEq)]
pub struct Reference {
    pub origin: Origin,
    pub name: String,
}

impl Reference {
    pub fn new(name: &str, origin: Origin) -> Reference {
        Reference {
            name: name.to_string(),
            origin,
        }
    }
    pub fn synthesize(&self) -> String {
        match &self.origin {
            Origin::Parameter => {
                format!("props.{}", camel_case(&self.name))
            }
            Origin::LogicalId { conditional } => format!(
                "{var}{chain}ref",
                var = camel_case(&self.name),
                chain = if *conditional { "?." } else { "." }
            ),
            Origin::Condition => camel_case(&self.name),
            Origin::PseudoParameter(x) => match x {
                PseudoParameter::Partition => String::from("this.partition"),
                PseudoParameter::Region => String::from("this.region"),
                PseudoParameter::StackId => String::from("this.stackId"),
                PseudoParameter::StackName => String::from("this.stackName"),
                PseudoParameter::URLSuffix => String::from("this.urlSuffix"),
                PseudoParameter::AccountId => String::from("this.account"),
                PseudoParameter::NotificationArns => String::from("this.notificationArns"),
            },
            Origin::GetAttribute {
                conditional,
                attribute,
            } => format!(
                "{var_name}{chain}attr{name}",
                var_name = camel_case(&self.name),
                chain = if *conditional { "?." } else { "." },
                name = pascal_case(attribute)
            ),
        }
    }
}

// Origin for the ReferenceTable
#[derive(Debug, Clone, PartialEq)]
pub enum Origin {
    Parameter,
    LogicalId {
        conditional: bool,
    },
    Condition,
    GetAttribute {
        attribute: String,
        conditional: bool,
    },
    PseudoParameter(PseudoParameter),
}

impl From<PseudoParameter> for Origin {
    fn from(pseudo: PseudoParameter) -> Self {
        Origin::PseudoParameter(pseudo)
    }
}

#[derive(Clone, Copy, Debug, PartialEq)]
pub enum PseudoParameter {
    Partition,
    Region,
    StackId,
    StackName,
    URLSuffix,
    AccountId,
    NotificationArns,
}

impl PseudoParameter {
    pub(super) fn try_from(name: &str) -> Option<Self> {
        match name {
            "AWS::AccountId" => Some(PseudoParameter::AccountId),
            "AWS::NotificationARNs" => Some(PseudoParameter::NotificationArns),
            "AWS::Partition" => Some(PseudoParameter::Partition),
            "AWS::Region" => Some(PseudoParameter::Region),
            "AWS::StackId" => Some(PseudoParameter::StackId),
            "AWS::StackName" => Some(PseudoParameter::StackName),
            "AWS::URLSuffix" => Some(PseudoParameter::URLSuffix),
            _ => None,
        }
    }
}
