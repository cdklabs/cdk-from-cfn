How to add a new test


1. Create a folder under end-to-end with the name of your new test


fail with error and tell developer to turn on 


if the template you want to test relies on referencing resources that already exist, also add a template that creates those dependency resources called deps-template.json.

The tests will check for a deps-template.json file and create a stack using that template first when testing that the original template is a valid cloudformation template.


import * as cdk from 'aws-cdk-lib';
import { StackUnderTest } from './stack-under-test';

const app = new cdk.App({
  analyticsReporting: false,
  defaultStackSynthesizer: new cdk.DefaultStackSynthesizer({
    generateBootstrapVersionRule: false,
  }),
});

new StackUnderTest(app, 'Stack', {});
