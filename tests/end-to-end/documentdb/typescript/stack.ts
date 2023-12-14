import * as cdk from 'aws-cdk-lib';
import * as docdb from 'aws-cdk-lib/aws-docdb';

export interface DocumentDbStackProps extends cdk.StackProps {
  /**
   * Cluster name
   * @default 'MyCluster'
   */
  readonly dbClusterName?: string;
  /**
   * Instance name
   * @default 'MyInstance'
   */
  readonly dbInstanceName?: string;
  /**
   * The database admin account username
   */
  readonly masterUser: string;
  /**
   * The database admin account password
   */
  readonly masterPassword: string;
  /**
   * Instance class. Please refer to: https://docs.aws.amazon.com/documentdb/latest/developerguide/db-instance-classes.html#db-instance-classes-by-region
   */
  readonly dbInstanceClass: string;
}

/**
 * AWS CloudFormation Sample Template DocumentDB_Quick_Create: Sample template showing how to create a DocumentDB DB cluster and DB instance. **WARNING** This template creates an Amazon DocumentDB resources and you will be billed for the AWS resources used if you create a stack from this template.
 */
export class DocumentDbStack extends cdk.Stack {
  public readonly clusterId;
  public readonly clusterEndpoint;
  public readonly clusterPort;
  public readonly engineVersion;

  public constructor(scope: cdk.App, id: string, props: DocumentDbStackProps) {
    super(scope, id, props);

    // Applying default props
    props = {
      ...props,
      dbClusterName: props.dbClusterName ?? 'MyCluster',
      dbInstanceName: props.dbInstanceName ?? 'MyInstance',
    };

    // Resources
    const dbCluster = new docdb.CfnDBCluster(this, 'DBCluster', {
      dbClusterIdentifier: props.dbClusterName!,
      masterUsername: props.masterUser!,
      masterUserPassword: props.masterPassword!,
      engineVersion: '4.0.0',
    });
    dbCluster.cfnOptions.deletionPolicy = cdk.CfnDeletionPolicy.DELETE;

    if (dbCluster == null) { throw new Error(`A combination of conditions caused 'dbCluster' to be undefined. Fixit.`); }
    const dbInstance = new docdb.CfnDBInstance(this, 'DBInstance', {
      dbClusterIdentifier: dbCluster.ref,
      dbInstanceIdentifier: props.dbInstanceName!,
      dbInstanceClass: props.dbInstanceClass!,
    });
    dbInstance.addDependency(dbCluster);

    // Outputs
    this.clusterId = dbCluster.ref;
    new cdk.CfnOutput(this, 'CfnOutputClusterId', {
      key: 'ClusterId',
      value: this.clusterId!.toString(),
    });
    this.clusterEndpoint = dbCluster.attrEndpoint;
    new cdk.CfnOutput(this, 'CfnOutputClusterEndpoint', {
      key: 'ClusterEndpoint',
      value: this.clusterEndpoint!.toString(),
    });
    this.clusterPort = dbCluster.attrPort;
    new cdk.CfnOutput(this, 'CfnOutputClusterPort', {
      key: 'ClusterPort',
      value: this.clusterPort!.toString(),
    });
    this.engineVersion = '4.0.0';
    new cdk.CfnOutput(this, 'CfnOutputEngineVersion', {
      key: 'EngineVersion',
      value: this.engineVersion!.toString(),
    });
  }
}
