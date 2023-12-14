// auto-generated! a human should update this!
import * as cdk from "aws-cdk-lib";
import { VpcStack } from "./stack";
const app = new cdk.App({
    defaultStackSynthesizer: new cdk.DefaultStackSynthesizer({
        generateBootstrapVersionRule: false,
    }),
});
new VpcStack(app, "Stack");
app.synth();
