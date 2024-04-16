// auto-generated! a human should update this!
import * as cdk from "aws-cdk-lib";
import { Ec2Stack } from "./stack";
const app = new cdk.App({
    defaultStackSynthesizer: new cdk.DefaultStackSynthesizer({
        generateBootstrapVersionRule: false,
    }),
});
new Ec2Stack(app, "Stack");
app.synth();
