// auto-generated! a human should update this!
import * as cdk from "aws-cdk-lib";
import { ApiGatewayV2Stack } from "./stack";
const app = new cdk.App({
    defaultStackSynthesizer: new cdk.DefaultStackSynthesizer({
        generateBootstrapVersionRule: false,
    }),
});
new ApiGatewayV2Stack(app, "Stack");
app.synth();
