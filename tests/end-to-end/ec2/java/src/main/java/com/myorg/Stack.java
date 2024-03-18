package com.myorg;

import software.constructs.Construct;

import java.util.*;
import software.amazon.awscdk.CfnMapping;
import software.amazon.awscdk.CfnTag;
import software.amazon.awscdk.Stack;
import software.amazon.awscdk.StackProps;

import software.amazon.awscdk.*;
import software.amazon.awscdk.services.ec2.*;

class Ec2Stack extends Stack {
    public Ec2Stack(final Construct scope, final String id) {
        super(scope, id, null);
    }

    public Ec2Stack(final Construct scope, final String id, final StackProps props) {
        super(scope, id, props);

        CfnVPC testVpc = CfnVPC.Builder.create(this, "TestVPC")
                .cidrBlock("10.0.0.0/16")
                .build();

        CfnSecurityGroup sg1 = CfnSecurityGroup.Builder.create(this, "SG1")
                .groupDescription("SG2")
                .vpcId(testVpc.getRef())
                .securityGroupEgress(Arrays.asList(
                        CfnSecurityGroup.EgressProperty.builder()
                                .ipProtocol("TCP")
                                .fromPort(10000)
                                .toPort(10000)
                                .cidrIp("10.0.0.0/16")
                                .build()))
                .build();

    }
}
