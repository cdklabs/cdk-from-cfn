import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import { Construct } from 'constructs';

export interface Ec2EncryptionConstructProps {
  /**
   * @default 'dev'
   */
  readonly environment?: string;
  /**
   * @default 'postgresql'
   */
  readonly databaseType?: string;
  /**
   * @default 'false'
   */
  readonly useEncryption?: boolean;
  /**
   * @default 'ami-1234567890abcdef0'
   */
  readonly encryptedAmi?: string;
  /**
   * @default 'ami-0987654321fedcba0'
   */
  readonly unencryptedAmi?: string;
  /**
   * @default 'Private1'
   */
  readonly subnetType?: string;
  /**
   * @default 'false'
   */
  readonly enableMonitoringParameter?: boolean;
}

export class Ec2EncryptionConstruct extends Construct {
  public constructor(scope: Construct, id: string, props: Ec2EncryptionConstructProps = {}) {
    super(scope, id);

    // Applying default props
    props = {
      ...props,
      environment: props.environment ?? 'dev',
      databaseType: props.databaseType ?? 'postgresql',
      useEncryption: props.useEncryption ?? false,
      encryptedAmi: props.encryptedAmi ?? 'ami-1234567890abcdef0',
      unencryptedAmi: props.unencryptedAmi ?? 'ami-0987654321fedcba0',
      subnetType: props.subnetType ?? 'Private1',
      enableMonitoringParameter: props.enableMonitoringParameter ?? false,
    };

    // Mappings
    const regionToAmi: Record<string, Record<string, string>> = {
      'us-east-1': {
        'AMI': 'ami-0c02fb55956c7d316',
      },
      'us-west-2': {
        'AMI': 'ami-008fe2fc65df48dac',
      },
      'eu-west-1': {
        'AMI': 'ami-0c9c942bd7bf113a2',
      },
      'ap-southeast-1': {
        'AMI': 'ami-0c802847a7dd848c0',
      },
      'us-east-2': {
        'AMI': 'ami-0900fe555666598a2',
      },
    };

    // Conditions
    const hasDatabase = props.databaseType! === 'mysql';
    const isProduction = props.environment! === 'prod';
    const usePrivateSecurityGroup = (props.subnetType! === 'Private1' || props.subnetType! === 'Private2');
    const keyPairProd = !isProduction;
    const useEncryption = (isProduction && hasDatabase);

    // Resources
    const privateSecurityGroup = new ec2.CfnSecurityGroup(this, 'PrivateSecurityGroup', {
      groupDescription: 'Private security group',
    });

    const publicSecurityGroup = new ec2.CfnSecurityGroup(this, 'PublicSecurityGroup', {
      groupDescription: 'Public security group',
    });

    const myApp = new ec2.CfnInstance(this, 'MyApp', {
      imageId: regionToAmi[cdk.Stack.of(this).region]['AMI'],
      instanceType: 't3.micro',
      tags: [
        {
          key: 'Name',
          value: cdk.Fn.select(1, 'My-EC2-Instance'.split('-')),
        },
      ],
      securityGroups: [
        usePrivateSecurityGroup ? privateSecurityGroup.ref : publicSecurityGroup.ref,
      ],
    });
  }
}
