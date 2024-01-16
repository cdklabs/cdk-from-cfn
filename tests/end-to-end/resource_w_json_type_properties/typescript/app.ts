// auto-generated! a human should update this!
import * as cdk from "aws-cdk-lib";
import { JsonPropsStack } from "./stack";
const app = new cdk.App({
    defaultStackSynthesizer: new cdk.DefaultStackSynthesizer({
        generateBootstrapVersionRule: false,
    }),
});
new JsonPropsStack(app, "Stack");
app.synth();
