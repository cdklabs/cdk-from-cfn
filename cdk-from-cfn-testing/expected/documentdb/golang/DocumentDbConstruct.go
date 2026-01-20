package main

import (
	cdk "github.com/aws/aws-cdk-go/awscdk/v2"
	docdb "github.com/aws/aws-cdk-go/awscdk/v2/awsdocdb"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"
)

type DocumentDbConstructProps struct {
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
type DocumentDbConstruct struct {
	constructs.Construct
	ClusterId interface{} // TODO: fix to appropriate type
	ClusterEndpoint interface{} // TODO: fix to appropriate type
	ClusterPort interface{} // TODO: fix to appropriate type
	EngineVersion interface{} // TODO: fix to appropriate type
}

func NewDocumentDbConstruct(scope constructs.Construct, id string, props *DocumentDbConstructProps) *DocumentDbConstruct {
	construct := constructs.NewConstruct(scope, &id)

	dbCluster := doc_db.NewCfnDBCluster(
		construct,
		jsii.String("DBCluster"),
		&doc_db.CfnDBClusterProps{
			DbClusterIdentifier: props.DbClusterName,
			MasterUsername: props.MasterUser,
			MasterUserPassword: props.MasterPassword,
			EngineVersion: jsii.String("4.0.0"),
		},
	)

	doc_db.NewCfnDBInstance(
		construct,
		jsii.String("DBInstance"),
		&doc_db.CfnDBInstanceProps{
			DbClusterIdentifier: dbCluster.Ref(),
			DbInstanceIdentifier: props.DbInstanceName,
			DbInstanceClass: props.DbInstanceClass,
		},
	)

	return &DocumentDbConstruct{
		Construct: construct,
		ClusterId: dbCluster.Ref(),
		ClusterEndpoint: dbCluster.AttrEndpoint(),
		ClusterPort: dbCluster.AttrPort(),
		EngineVersion: jsii.String("4.0.0"),
	}
}

