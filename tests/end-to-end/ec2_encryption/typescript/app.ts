// auto-generated! a human should update this!
import * as cdk from "aws-cdk-lib";
import { Ec2EncryptionStack } from "./stack";
const app = new cdk.App({
    defaultStackSynthesizer: new cdk.DefaultStackSynthesizer({
        generateBootstrapVersionRule: false,
    }),
});
new Ec2EncryptionStack(app, "Stack");
app.synth();
