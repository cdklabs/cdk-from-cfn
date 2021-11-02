#[derive(Debug, Clone)]
pub struct Reference {
    pub origin: Origin,
    pub name: String,
}

impl Reference {
    fn synthesize(&self) -> String {
        match &self.origin {
            Origin::Parameter => {
                format!("props.{}", self.name)
            }
            Origin::LogicalId => self.name.to_string(),
            Origin::Condition => self.name.to_string(),
            Origin::PseudoParameter(x) => match x {
                PseudoParameter::Partition => String::from("this.partition"),
                PseudoParameter::Region => String::from("this.region"),
                PseudoParameter::StackId => String::from("this.stackId"),
                PseudoParameter::StackName => String::from("this.stackName"),
                PseudoParameter::URLSuffix => String::from("this.urlSuffix"),
            },
        }
    }

    pub fn match_pseudo_parameter(val: &str) -> Option<PseudoParameter> {
        let pseudo = match val {
            "AWS::Region" => PseudoParameter::Region,
            "AWS::Partition" => PseudoParameter::Partition,
            "AWS::StackName" => PseudoParameter::StackName,
            "AWS::UrlSuffix" => PseudoParameter::URLSuffix,
            "AWS::StackId" => PseudoParameter::StackId,
            &_ => return Option::None,
        };

        Option::Some(pseudo)
    }
}

// Origin for the ReferenceTable
#[derive(Debug, Clone)]
pub enum Origin {
    Parameter,
    LogicalId,
    Condition,
    PseudoParameter(PseudoParameter),
}

#[derive(Debug, Clone)]
pub enum PseudoParameter {
    Partition,
    Region,
    StackId,
    StackName,
    URLSuffix,
}
