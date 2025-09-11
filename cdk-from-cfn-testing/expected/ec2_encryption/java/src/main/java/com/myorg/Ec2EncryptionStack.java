package com.myorg;

import software.constructs.Construct;

import java.util.*;
import software.amazon.awscdk.CfnMapping;
import software.amazon.awscdk.CfnTag;
import software.amazon.awscdk.Stack;
import software.amazon.awscdk.StackProps;

import software.amazon.awscdk.*;
import software.amazon.awscdk.services.ec2.*;

class Ec2EncryptionStack extends Stack {
    public Ec2EncryptionStack(final Construct scope, final String id) {
        super(scope, id, null);
    }

    public Ec2EncryptionStack(final Construct scope, final String id, final StackProps props) {
        this(scope, id, props, null, null, null, null, null, null, null);
    }

    public Ec2EncryptionStack(final Construct scope, final String id, final StackProps props,
            String environment,
            String databaseType,
            Boolean useEncryption,
            String encryptedAmi,
            String unencryptedAmi,
            String subnetType,
            Boolean enableMonitoringParameter) {
        super(scope, id, props);

        environment = Optional.ofNullable(environment).isPresent() ? environment
                : "dev";
        databaseType = Optional.ofNullable(databaseType).isPresent() ? databaseType
                : "postgresql";
        useEncryption = Optional.ofNullable(useEncryption).isPresent() ? useEncryption
                : false;
        encryptedAmi = Optional.ofNullable(encryptedAmi).isPresent() ? encryptedAmi
                : "ami-1234567890abcdef0";
        unencryptedAmi = Optional.ofNullable(unencryptedAmi).isPresent() ? unencryptedAmi
                : "ami-0987654321fedcba0";
        subnetType = Optional.ofNullable(subnetType).isPresent() ? subnetType
                : "Private1";
        enableMonitoringParameter = Optional.ofNullable(enableMonitoringParameter).isPresent() ? enableMonitoringParameter
                : false;
        // Mappings
        final CfnMapping regionToAmi = new CfnMapping(this, "regionToAmi");
        regionToAmi.setValue("us-east-1", "AMI", "ami-0c02fb55956c7d316");
        regionToAmi.setValue("us-west-2", "AMI", "ami-008fe2fc65df48dac");
        regionToAmi.setValue("eu-west-1", "AMI", "ami-0c9c942bd7bf113a2");
        regionToAmi.setValue("ap-southeast-1", "AMI", "ami-0c802847a7dd848c0");
        regionToAmi.setValue("us-east-2", "AMI", "ami-0900fe555666598a2");

        Boolean hasDatabase = databaseType.equals("mysql");
        Boolean isProduction = environment.equals("prod");
        Boolean usePrivateSecurityGroup = (subnetType.equals("Private1") || subnetType.equals("Private2"));
        Boolean keyPairProd = !IsProduction;
        Boolean useEncryption = (IsProduction && HasDatabase);

        CfnSecurityGroup privateSecurityGroup = CfnSecurityGroup.Builder.create(this, "PrivateSecurityGroup")
                .groupDescription("Private security group")
                .build();

        CfnSecurityGroup publicSecurityGroup = CfnSecurityGroup.Builder.create(this, "PublicSecurityGroup")
                .groupDescription("Public security group")
                .build();

        CfnInstance myApp = CfnInstance.Builder.create(this, "MyApp")
                .imageId(regionToAmi.findInMap(this.getRegion(), "AMI"))
                .instanceType("t3.micro")
                .tags(Arrays.asList(
                        CfnTag.builder()
                                .key("Name")
                                .value(Fn.select(1, My-EC2-Instance.split("-")))
                                .build()))
                .securityGroups(Arrays.asList(
                        usePrivateSecurityGroup ? privateSecurityGroup.getRef()
                                : publicSecurityGroup.getRef()))
                .build();

    }
}
