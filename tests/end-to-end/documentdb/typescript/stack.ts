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
   * @default 'MainUser'
   */
  readonly masterUser?: string;
  /**
   * The database admin account password
   * @default 'password'
   */
  readonly masterPassword?: string;
  /**
   * Instance class. Please refer to: https://docs.aws.amazon.com/documentdb/latest/developerguide/db-instance-classes.html#db-instance-classes-by-region
   * @default 'db.t3.medium'
   */
  readonly dbInstanceClass?: string;
}

/**
 * AWS CloudFormation Sample Template DocumentDB_Quick_Create: Sample template showing how to create a DocumentDB DB cluster and DB instance. **WARNING** This template creates an Amazon DocumentDB resources and you will be billed for the AWS resources used if you create a stack from this template.
 */
export class DocumentDbStack extends cdk.Stack {
  public readonly clusterId;
  public readonly clusterEndpoint;
  public readonly clusterPort;
  public readonly engineVersion;

  public constructor(scope: cdk.App, id: string, props: DocumentDbStackProps = {}) {
    super(scope, id, props);

    // Applying default props
    props = {
      ...props,
      dbClusterName: props.dbClusterName ?? 'MyCluster',
      dbInstanceName: props.dbInstanceName ?? 'MyInstance',
      masterUser: new cdk.CfnParameter(this, 'MasterUser', {
        type: 'String',
        default: props.masterUser?.toString() ?? 'MainUser',
        description: 'The database admin account username',
        noEcho: true,
      }).valueAsString,
      masterPassword: new cdk.CfnParameter(this, 'MasterPassword', {
        type: 'String',
        default: props.masterPassword?.toString() ?? 'password',
        description: 'The database admin account password',
        noEcho: true,
      }).valueAsString,
      dbInstanceClass: props.dbInstanceClass ?? 'db.t3.medium',
    };

    // Resources
    const dbCluster = new docdb.CfnDBCluster(this, 'DBCluster', {
      dbClusterIdentifier: props.dbClusterName!,
      masterUsername: props.masterUser!,
      masterUserPassword: props.masterPassword!,
      engineVersion: '4.0.0',
    });
    dbCluster.cfnOptions.deletionPolicy = cdk.CfnDeletionPolicy.DELETE;

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
