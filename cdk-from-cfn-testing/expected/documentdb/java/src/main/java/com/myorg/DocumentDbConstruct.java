package com.myorg;

import software.constructs.Construct;

import java.util.*;
import software.amazon.awscdk.CfnMapping;
import software.amazon.awscdk.CfnTag;
import software.amazon.awscdk.Stack;
import software.amazon.awscdk.StackProps;

import software.amazon.awscdk.*;
import software.amazon.awscdk.services.docdb.*;

class DocumentDbConstruct extends Construct {
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

    public DocumentDbConstruct(final Construct scope, final String id) {
        this(scope, id, null, null, null, null, null);
    }

    public DocumentDbConstruct(final Construct scope, final String id,
            String dbClusterName,
            String dbInstanceName,
            String masterUser,
            String masterPassword,
            String dbInstanceClass) {
        super(scope, id);

        dbClusterName = Optional.ofNullable(dbClusterName).isPresent() ? dbClusterName
                : "MyCluster";
        dbInstanceName = Optional.ofNullable(dbInstanceName).isPresent() ? dbInstanceName
                : "MyInstance";
        masterUser = Optional.ofNullable(masterUser).isPresent()
                ? masterUser
                : CfnParameter.Builder.create(this, "MasterUser")
                        .type("String")
                        .defaultValue("MainUser")
                        .noEcho(true)
                        .build()
                        .getValueAsString();

        masterPassword = Optional.ofNullable(masterPassword).isPresent()
                ? masterPassword
                : CfnParameter.Builder.create(this, "MasterPassword")
                        .type("String")
                        .defaultValue("password")
                        .noEcho(true)
                        .build()
                        .getValueAsString();

        dbInstanceClass = Optional.ofNullable(dbInstanceClass).isPresent() ? dbInstanceClass
                : "db.t3.medium";

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
        CfnOutput.Builder.create(this, "CfnOutputClusterId")
                .key("ClusterId")
                .value(this.clusterId.toString())
                .build();

        this.clusterEndpoint = dbCluster.getAttrEndpoint();
        CfnOutput.Builder.create(this, "CfnOutputClusterEndpoint")
                .key("ClusterEndpoint")
                .value(this.clusterEndpoint.toString())
                .build();

        this.clusterPort = dbCluster.getAttrPort();
        CfnOutput.Builder.create(this, "CfnOutputClusterPort")
                .key("ClusterPort")
                .value(this.clusterPort.toString())
                .build();

        this.engineVersion = "4.0.0";
        CfnOutput.Builder.create(this, "CfnOutputEngineVersion")
                .key("EngineVersion")
                .value(this.engineVersion.toString())
                .build();

    }
}
