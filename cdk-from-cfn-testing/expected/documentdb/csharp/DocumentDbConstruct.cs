using Amazon.CDK;
using Amazon.CDK.AWS.DocDB;
using Constructs;
using System.Collections.Generic;

namespace DocumentDbConstruct
{
    public class DocumentDbConstructProps
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
    public class DocumentDbConstruct : Construct
    {
        public object ClusterId { get; } 

        public object ClusterEndpoint { get; } 

        public object ClusterPort { get; } 

        public object EngineVersion { get; } 

        public DocumentDbConstruct(Construct scope, string id, DocumentDbConstructProps props = null) : base(scope, id)
        {
            // Applying default props
            props ??= new DocumentDbConstructProps();
            props.DbClusterName ??= "MyCluster";
            props.DbInstanceName ??= "MyInstance";
            props.MasterUser = new CfnParameter(this, "MasterUser", new CfnParameterProps
            {
                Type = "String",
                Default = props.MasterUser ?? "MainUser",
                Description = "The database admin account username",
                NoEcho = true,
            }).ValueAsString;
            props.MasterPassword = new CfnParameter(this, "MasterPassword", new CfnParameterProps
            {
                Type = "String",
                Default = props.MasterPassword ?? "password",
                Description = "The database admin account password",
                NoEcho = true,
            }).ValueAsString;
            props.DbInstanceClass ??= "db.t3.medium";


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
