#[derive(Debug, Clone, PartialEq)]
pub struct Reference {
    pub origin: Origin,
    pub name: String,
}

impl Reference {
    #[inline]
    pub fn new(name: &str, origin: Origin) -> Reference {
        Reference {
            name: name.to_string(),
            origin,
        }
    }
}

// Origin for the ReferenceTable
#[derive(Debug, Clone, PartialEq)]
pub enum Origin {
    CfnParameter,
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
    #[inline]
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
