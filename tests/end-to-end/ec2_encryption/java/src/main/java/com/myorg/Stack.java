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
        this(scope, id, props, null, null, null, null, null);
    }

    public Ec2EncryptionStack(final Construct scope, final String id, final StackProps props,
            String environment,
            String databaseType,
            Boolean useEncryption,
            String encryptedAmi,
            String unencryptedAmi) {
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
        Boolean hasDatabase = databaseType.equals("mysql");
        Boolean isProduction = environment.equals("prod");
        Boolean useEncryption = (IsProduction && HasDatabase);

        CfnInstance myApp = CfnInstance.Builder.create(this, "MyApp")
                .imageId(useEncryption ? encryptedAmi
                        : unencryptedAmi)
                .build();

    }
}
