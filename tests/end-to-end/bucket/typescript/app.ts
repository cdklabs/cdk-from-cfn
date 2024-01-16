// auto-generated! a human should update this!
import * as cdk from "aws-cdk-lib";
import { BucketStack } from "./stack";
const app = new cdk.App({
    defaultStackSynthesizer: new cdk.DefaultStackSynthesizer({
        generateBootstrapVersionRule: false,
    }),
});
new BucketStack(app, "Stack");
app.synth();
