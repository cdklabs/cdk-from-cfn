from aws_cdk import Stack
import aws_cdk as cdk
import aws_cdk.aws_docdb as docdb
from constructs import Construct

"""
  AWS CloudFormation Sample Template DocumentDB_Quick_Create: Sample template showing how to create a DocumentDB DB cluster and DB instance. **WARNING** This template creates an Amazon DocumentDB resources and you will be billed for the AWS resources used if you create a stack from this template.
"""
class DocumentDbStack(Stack):
  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    # Applying default props
    props = {
      'dbClusterName': kwargs.get('dbClusterName', 'MyCluster'),
      'dbInstanceName': kwargs.get('dbInstanceName', 'MyInstance'),
    }

    # Resources
    dbCluster = docdb.CfnDBCluster(self, 'DBCluster',
          db_cluster_identifier = props['dbClusterName'],
          master_username = props['masterUser'],
          master_user_password = props['masterPassword'],
          engine_version = '4.0.0',
        )
    dbCluster.cfn_options.deletion_policy = cdk.CfnDeletionPolicy.DELETE

    dbInstance = docdb.CfnDBInstance(self, 'DBInstance',
          db_cluster_identifier = dbCluster.ref,
          db_instance_identifier = props['dbInstanceName'],
          db_instance_class = props['dbInstanceClass'],
        )
    dbInstance.add_dependency(dbCluster)

    # Outputs
    self.cluster_id = dbCluster.ref
    cdk.CfnOutput(self, 'CfnOutputClusterId', 
      key = 'ClusterId',
      value = str(self.cluster_id),
    )

    self.cluster_endpoint = dbCluster.attr_endpoint
    cdk.CfnOutput(self, 'CfnOutputClusterEndpoint', 
      key = 'ClusterEndpoint',
      value = str(self.cluster_endpoint),
    )

    self.cluster_port = dbCluster.attr_port
    cdk.CfnOutput(self, 'CfnOutputClusterPort', 
      key = 'ClusterPort',
      value = str(self.cluster_port),
    )

    self.engine_version = '4.0.0'
    cdk.CfnOutput(self, 'CfnOutputEngineVersion', 
      key = 'EngineVersion',
      value = str(self.engine_version),
    )



