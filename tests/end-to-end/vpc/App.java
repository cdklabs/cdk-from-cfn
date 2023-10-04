package com.myorg;

import software.constructs.Construct;

import java.util.*;
import software.amazon.awscdk.CfnMapping;
import software.amazon.awscdk.CfnTag;
import software.amazon.awscdk.Stack;
import software.amazon.awscdk.StackProps;

import software.amazon.awscdk.*;
import software.amazon.awscdk.services.ec2.*;

class VpcStack extends Stack {
    public VpcStack(final Construct scope, final String id) {
        super(scope, id, null);
    }

    public VpcStack(final Construct scope, final String id, final StackProps props) {
        super(scope, id, props);

        CfnVPC vpc = CfnVPC.Builder.create(this, "VPC")
                .cidrBlock("10.42.0.0/16")
                .enableDnsSupport(true)
                .enableDnsHostnames(true)
                .tags(Arrays.asList(
                        CfnTag.builder()
                                .key("cost-center")
                                .value(String.valueOf(1337))
                                .build()))
                .build();

        CfnSubnet subnet1 = CfnSubnet.Builder.create(this, "Subnet1")
                .availabilityZone(Fn.select(0, Fn.getAzs("")))
                .cidrBlock(Fn.select(0, Fn.cidr(vpc.getAttrCidrBlock(), 6, "8")))
                .vpcId(vpc.getRef())
                .build();

        CfnSubnet subnet2 = CfnSubnet.Builder.create(this, "Subnet2")
                .availabilityZone(Fn.select(1, Fn.getAzs("")))
                .cidrBlock(Fn.select(1, Fn.cidr(vpc.getAttrCidrBlock(), 6, "8")))
                .vpcId(vpc.getRef())
                .build();

        CfnSubnet subnet3 = CfnSubnet.Builder.create(this, "Subnet3")
                .availabilityZone(Fn.select(2, Fn.getAzs("")))
                .cidrBlock(Fn.select(2, Fn.cidr(vpc.getAttrCidrBlock(), 6, "8")))
                .vpcId(vpc.getRef())
                .build();

    }
}
