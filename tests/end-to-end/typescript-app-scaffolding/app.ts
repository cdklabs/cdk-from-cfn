import * as cdk from 'aws-cdk-lib';
import { StackUnderTest } from './stack-under-test';

const app = new cdk.App({
  analyticsReporting: false,
  defaultStackSynthesizer: new cdk.DefaultStackSynthesizer({
    generateBootstrapVersionRule: false,
  }),
});

new StackUnderTest(app, 'Stack', {
  
});
app.synth();
