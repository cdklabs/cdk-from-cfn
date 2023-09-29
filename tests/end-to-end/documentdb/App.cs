using Amazon.CDK;
using Amazon.CDK.AWS.docdb;
using Constructs;
using System.Collections.Generic;

namespace DocumentDbStack
{
    public class DocumentDbStackProps : StackProps
    {
        /// <summary>
        /// Cluster name
        /// </summary>
        public string DbClusterName { get; set; }

        /// <summary>
        /// Instance name
        /// </summary>
        public string DbInstanceName { get; set; }

        /// <summary>
        /// The database admin account username
        /// </summary>
        public string MasterUser { get; set; }

        /// <summary>
        /// The database admin account password
        /// </summary>
        public string MasterPassword { get; set; }

        /// <summary>
        /// Instance class. Please refer to: https://docs.aws.amazon.com/documentdb/latest/developerguide/db-instance-classes.html#db-instance-classes-by-region
        /// </summary>
        public string DbInstanceClass { get; set; }

    }

    /// <summary>
    /// AWS CloudFormation Sample Template DocumentDB_Quick_Create: Sample template showing how to create a DocumentDB DB cluster and DB instance. **WARNING** This template creates an Amazon DocumentDB resources and you will be billed for the AWS resources used if you create a stack from this template.
    /// </summary>
    public class DocumentDbStack : Stack
    {
        public object ClusterId { get; } 

        public object ClusterEndpoint { get; } 

        public object ClusterPort { get; } 

        public object EngineVersion { get; } 

        public DocumentDbStack(Construct scope, string id, DocumentDbStackProps props = null) : base(scope, id, props)
        {
            // Applying default props
            props.DbClusterName ??= "MyCluster";
            props.DbInstanceName ??= "MyInstance";


            // Resources
            var dbCluster = new CfnDBCluster(this, "DBCluster", new CfnDBClusterProps
            {
                DbClusterIdentifier = props.DbClusterName,
                MasterUsername = props.MasterUser,
                MasterUserPassword = props.MasterPassword,
                EngineVersion = "4.0.0",
            });
            var dbInstance = new CfnDBInstance(this, "DBInstance", new CfnDBInstanceProps
            {
                DbClusterIdentifier = dbCluster.Ref,
                DbInstanceIdentifier = props.DbInstanceName,
                DbInstanceClass = props.DbInstanceClass,
            });

            // Outputs
            ClusterId = dbCluster.Ref;
            ClusterEndpoint = dbCluster.AttrEndpoint;
            ClusterPort = dbCluster.AttrPort;
            EngineVersion = "4.0.0";
        }
    }
}
