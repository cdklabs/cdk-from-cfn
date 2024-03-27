using Amazon.CDK;
using Amazon.CDK.AWS.IAM;
using Constructs;
using System.Collections.Generic;

namespace StackSetStack
{
    public class StackSetStackProps : StackProps
    {
        public string ModuleName { get; set; }

        public string RoleName { get; set; }

        public string RolePath { get; set; }

    }

    /// <summary>
    /// Deploy required components for StackSet custom resources in this region.  Lambda ARN is exported as StackSetCustomResource
    /// </summary>
    public class StackSetStack : Stack
    {
        public StackSetStack(Construct scope, string id, StackSetStackProps props = null) : base(scope, id, props)
        {
            // Applying default props
            props ??= new StackSetStackProps();
            props.ModuleName ??= "lambda_function";
            props.RoleName ??= "";
            props.RolePath ??= "";


            // Conditions
            bool useRoleName = !(props.RoleName == "");
            bool useRolePath = !(props.RolePath == "");

            // Resources
            var stackSetResourceRole = new CfnRole(this, "StackSetResourceRole", new CfnRoleProps
            {
                RoleName = useRoleName ? props.RoleName : null,
                Path = useRolePath ? props.RolePath : "/",
                AssumeRolePolicyDocument = new Dictionary<string, object>
                {
                    { "Version", "2012-10-17"},
                    { "Statement", new []
                    {
                        new Dictionary<string, object>
                        {
                            { "Effect", "Allow"},
                            { "Principal", new Dictionary<string, object>
                            {
                                { "Service", "lambda.amazonaws.com"},
                            }},
                            { "Action", "sts:AssumeRole"},
                        },
                    }},
                },
                Policies = new []
                {
                    new CfnRole.PolicyProperty
                    {
                        PolicyName = "IAMPassRolePermissions",
                        PolicyDocument = new Dictionary<string, object>
                        {
                            { "Version", "2012-10-17"},
                            { "Statement", new []
                            {
                                new Dictionary<string, object>
                                {
                                    { "Effect", "Allow"},
                                    { "Action", "iam:PassRole"},
                                    { "Resource", "*"},
                                },
                            }},
                        },
                    },
                    new CfnRole.PolicyProperty
                    {
                        PolicyName = "CloudFormationPermissions",
                        PolicyDocument = new Dictionary<string, object>
                        {
                            { "Version", "2012-10-17"},
                            { "Statement", new []
                            {
                                new Dictionary<string, object>
                                {
                                    { "Effect", "Allow"},
                                    { "Action", "cloudformation:*"},
                                    { "Resource", "*"},
                                },
                            }},
                        },
                    },
                    new CfnRole.PolicyProperty
                    {
                        PolicyName = "LambdaPermissions",
                        PolicyDocument = new Dictionary<string, object>
                        {
                            { "Version", "2012-10-17"},
                            { "Statement", new []
                            {
                                new Dictionary<string, object>
                                {
                                    { "Effect", "Allow"},
                                    { "Action", "logs:CreateLogGroup"},
                                    { "Resource", new []
                                    {
                                        $"arn:aws:logs:{Region}:{Account}:*",
                                    }},
                                },
                                new Dictionary<string, object>
                                {
                                    { "Effect", "Allow"},
                                    { "Action", new []
                                    {
                                        "logs:CreateLogStream",
                                        "logs:PutLogEvents",
                                    }},
                                    { "Resource", new []
                                    {
                                        $"arn:aws:logs:{Region}:{Account}:log-group:/aws/lambda/*",
                                    }},
                                },
                            }},
                        },
                    },
                    new CfnRole.PolicyProperty
                    {
                        PolicyName = "S3Permissions",
                        PolicyDocument = new Dictionary<string, object>
                        {
                            { "Version", "2012-10-17"},
                            { "Statement", new []
                            {
                                new Dictionary<string, object>
                                {
                                    { "Effect", "Allow"},
                                    { "Action", new []
                                    {
                                        "s3:Get*",
                                        "s3:List*",
                                    }},
                                    { "Resource", "*"},
                                },
                            }},
                        },
                    },
                },
            });
        }
    }
}
