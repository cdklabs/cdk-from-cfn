package documentdb

import (
	cdk "github.com/aws/aws-cdk-go/awscdk/v2"
	docdb "github.com/aws/aws-cdk-go/awscdk/v2/awsdocdb"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"
)

type DocumentDbStackProps struct {
	cdk.StackProps
	/// Cluster name
	DbClusterName *string
	/// Instance name
	DbInstanceName *string
	/// The database admin account username
	MasterUser *string
	/// The database admin account password
	MasterPassword *string
	/// Instance class. Please refer to: https://docs.aws.amazon.com/documentdb/latest/developerguide/db-instance-classes.html#db-instance-classes-by-region
	DbInstanceClass *string
}

/// AWS CloudFormation Sample Template DocumentDB_Quick_Create: Sample template showing how to create a DocumentDB DB cluster and DB instance. **WARNING** This template creates an Amazon DocumentDB resources and you will be billed for the AWS resources used if you create a stack from this template.
type DocumentDbStack struct {
	cdk.Stack
	ClusterId interface{} // TODO: fix to appropriate type
	ClusterEndpoint interface{} // TODO: fix to appropriate type
	ClusterPort interface{} // TODO: fix to appropriate type
	EngineVersion interface{} // TODO: fix to appropriate type
}

func NewDocumentDbStack(scope constructs.Construct, id string, props DocumentDbStackProps) *DocumentDbStack {
	stack := cdk.NewStack(scope, &id, &props.StackProps)

	dbCluster := doc_db.NewCfnDBCluster(
		stack,
		jsii.String("DBCluster"),
		&doc_db.CfnDBClusterProps{
			DbClusterIdentifier: props.DbClusterName,
			MasterUsername: props.MasterUser,
			MasterUserPassword: props.MasterPassword,
			EngineVersion: jsii.String("4.0.0"),
		},
	)

	doc_db.NewCfnDBInstance(
		stack,
		jsii.String("DBInstance"),
		&doc_db.CfnDBInstanceProps{
			DbClusterIdentifier: dbCluster.Ref(),
			DbInstanceIdentifier: props.DbInstanceName,
			DbInstanceClass: props.DbInstanceClass,
		},
	)

	return &DocumentDbStack{
		Stack: stack,
		ClusterId: dbCluster.Ref(),
		ClusterEndpoint: dbCluster.AttrEndpoint(),
		ClusterPort: dbCluster.AttrPort(),
		EngineVersion: jsii.String("4.0.0"),
	}
}

func main() {
	defer jsii.Close()

	app := cdk.NewApp(nil)

	NewDocumentDbStack(app, "DocumentDb", DocumentDbStackProps{
		cdk.StackProps{
			Env: env(),
		},
		DbClusterName: "MyCluster",
		DbInstanceName: "MyInstance",
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
