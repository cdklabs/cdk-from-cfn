package vpc

import (
	cdk "github.com/aws/aws-cdk-go/awscdk/v2"
	ec2 "github.com/aws/aws-cdk-go/awscdk/v2/awsec2"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"
)

type VpcStackProps struct {
	cdk.StackProps
}

type VpcStack struct {
	cdk.Stack
}

func NewVpcStack(scope constructs.Construct, id string, props VpcStackProps) *VpcStack {
	stack := cdk.NewStack(scope, &id, &props.StackProps)

	vpc := ec2.NewCfnVPC(
		stack,
		jsii.String("VPC"),
		&ec2.CfnVPCProps{
			CidrBlock: jsii.String("10.42.0.0/16"),
			EnableDnsSupport: jsii.Bool(true),
			EnableDnsHostnames: jsii.Bool(true),
			Tags: &[]*cdk.CfnTag{
				&cdk.CfnTag{
					Key: jsii.String("cost-center"),
					Value: jsii.Number(1337),
				},
			},
		},
	)

	ec2.NewCfnSubnet(
		stack,
		jsii.String("Subnet1"),
		&ec2.CfnSubnetProps{
			AvailabilityZone: cdk.Fn_Select(jsii.Number(0), cdk.Fn_GetAzs(jsii.String(""))),
			CidrBlock: cdk.Fn_Select(jsii.Number(0), cdk.Fn_Cidr(vpc.AttrCidrBlock(), jsii.Number(6), jsii.String("8"))),
			VpcId: vpc.Ref(),
		},
	)

	ec2.NewCfnSubnet(
		stack,
		jsii.String("Subnet2"),
		&ec2.CfnSubnetProps{
			AvailabilityZone: cdk.Fn_Select(jsii.Number(1), cdk.Fn_GetAzs(jsii.String(""))),
			CidrBlock: cdk.Fn_Select(jsii.Number(1), cdk.Fn_Cidr(vpc.AttrCidrBlock(), jsii.Number(6), jsii.String("8"))),
			VpcId: vpc.Ref(),
		},
	)

	ec2.NewCfnSubnet(
		stack,
		jsii.String("Subnet3"),
		&ec2.CfnSubnetProps{
			AvailabilityZone: cdk.Fn_Select(jsii.Number(2), cdk.Fn_GetAzs(jsii.String(""))),
			CidrBlock: cdk.Fn_Select(jsii.Number(2), cdk.Fn_Cidr(vpc.AttrCidrBlock(), jsii.Number(6), jsii.String("8"))),
			VpcId: vpc.Ref(),
		},
	)

	return &VpcStack{
		Stack: stack,
	}
}

func main() {
	defer jsii.Close()

	app := cdk.NewApp(nil)

	NewVpcStack(app, "Vpc", VpcStackProps{
		cdk.StackProps{
			Env: env(),
		},
	})

	app.Synth(nil)
}

// env determines the AWS environment (account+region) in which our stack is to
// be deployed. For more information see: https://docs.aws.amazon.com/cdk/latest/guide/environments.html
func env() *cdk.Environment {
	// If unspecified, this stack will be "environment-agnostic".
	// Account/Region-dependent features and context lookups will not work, but a
	// single synthesized template can be deployed anywhere.
	//---------------------------------------------------------------------------
	return nil

	// Uncomment if you know exactly what account and region you want to deploy
	// the stack to. This is the recommendation for production stacks.
	//---------------------------------------------------------------------------
	// return &cdk.Environment{
	//  Account: jsii.String("123456789012"),
	//  Region:  jsii.String("us-east-1"),
	// }

	// Uncomment to specialize this stack for the AWS Account and Region that are
	// implied by the current CLI configuration. This is recommended for dev
	// stacks.
	//---------------------------------------------------------------------------
	// return &cdk.Environment{
	//  Account: jsii.String(os.Getenv("CDK_DEFAULT_ACCOUNT")),
	//  Region:  jsii.String(os.Getenv("CDK_DEFAULT_REGION")),
	// }
}
