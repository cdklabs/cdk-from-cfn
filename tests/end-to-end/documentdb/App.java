package com.myorg;

import software.constructs.Construct;

import java.util.*;
import software.amazon.awscdk.CfnMapping;
import software.amazon.awscdk.CfnTag;
import software.amazon.awscdk.Stack;
import software.amazon.awscdk.StackProps;

import software.amazon.awscdk.*;
import software.amazon.awscdk.services.docdb.*;

class DocumentDbStack extends Stack {
    private Object clusterId;

    private Object clusterEndpoint;

    private Object clusterPort;

    private Object engineVersion;

    public Object getClusterId() {
        return this.clusterId;
    }

    public Object getClusterEndpoint() {
        return this.clusterEndpoint;
    }

    public Object getClusterPort() {
        return this.clusterPort;
    }

    public Object getEngineVersion() {
        return this.engineVersion;
    }

    public DocumentDbStack(final Construct scope, final String id) {
        super(scope, id, null);
    }

    public DocumentDbStack(final Construct scope, final String id, final StackProps props) {
        this(scope, id, props, null, null, null, null, null);
    }

    public DocumentDbStack(final Construct scope, final String id, final StackProps props,
            String dbClusterName,
            String dbInstanceName,
            String masterUser,
            String masterPassword,
            String dbInstanceClass) {
        super(scope, id, props);

        dbClusterName = Optional.ofNullable(dbClusterName).isPresent() ? dbClusterName
                : "MyCluster";
        dbInstanceName = Optional.ofNullable(dbInstanceName).isPresent() ? dbInstanceName
                : "MyInstance";




        CfnDBCluster dbCluster = CfnDBCluster.Builder.create(this, "DBCluster")
                .dbClusterIdentifier(dbClusterName)
                .masterUsername(masterUser)
                .masterUserPassword(masterPassword)
                .engineVersion("4.0.0")
                .build();

        dbCluster.applyRemovalPolicy(RemovalPolicy.DESTROY);

        CfnDBInstance dbInstance = CfnDBInstance.Builder.create(this, "DBInstance")
                .dbClusterIdentifier(dbCluster.getRef())
                .dbInstanceIdentifier(dbInstanceName)
                .dbInstanceClass(dbInstanceClass)
                .build();

        dbInstance.addDependency(dbCluster);

        this.clusterId = dbCluster.getRef();
        CfnOutput.Builder.create(this, "ClusterId")
                .value(this.clusterId.toString())
                .build();

        this.clusterEndpoint = dbCluster.getAttrEndpoint();
        CfnOutput.Builder.create(this, "ClusterEndpoint")
                .value(this.clusterEndpoint.toString())
                .build();

        this.clusterPort = dbCluster.getAttrPort();
        CfnOutput.Builder.create(this, "ClusterPort")
                .value(this.clusterPort.toString())
                .build();

        this.engineVersion = "4.0.0";
        CfnOutput.Builder.create(this, "EngineVersion")
                .value(this.engineVersion.toString())
                .build();

    }
}
