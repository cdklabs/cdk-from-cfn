package com.myorg;

import software.constructs.Construct;

import java.util.*;
import software.amazon.awscdk.CfnMapping;
import software.amazon.awscdk.CfnTag;
import software.amazon.awscdk.Stack;
import software.amazon.awscdk.StackProps;

import software.amazon.awscdk.*;
import software.amazon.awscdk.services.efs.*;

class EfsStack extends Stack {
    public EfsStack(final Construct scope, final String id) {
        super(scope, id, null);
    }

    public EfsStack(final Construct scope, final String id, final StackProps props) {
        super(scope, id, props);

        CfnFileSystem fileSystem = CfnFileSystem.Builder.create(this, "FileSystem")
                .build();

    }
}
