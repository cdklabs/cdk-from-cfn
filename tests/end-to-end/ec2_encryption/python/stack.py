from aws_cdk import Stack
import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2
from constructs import Construct

class Ec2EncryptionStack(Stack):
  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    # Applying default props
    props = {
      'environment': kwargs.get('environment', 'dev'),
      'databaseType': kwargs.get('databaseType', 'postgresql'),
      'useEncryption': kwargs.get('useEncryption', False),
      'encryptedAmi': kwargs.get('encryptedAmi', 'ami-1234567890abcdef0'),
      'unencryptedAmi': kwargs.get('unencryptedAmi', 'ami-0987654321fedcba0'),
      'subnetType': kwargs.get('subnetType', 'Private1'),
      'enableMonitoringParameter': kwargs.get('enableMonitoringParameter', False),
    }

    # Mappings
    regionToAmi = {
      'us-east-1': {
        'AMI': 'ami-12345678',
      },
      'us-west-2': {
        'AMI': 'ami-87654321',
      },
    }

    # Conditions
    has_database = props['databaseType'] == 'mysql'
    is_production = props['environment'] == 'prod'
    use_private_security_group = (props['subnetType'] == 'Private1' or props['subnetType'] == 'Private2')
    key_pair_prod = not is_production
    use_encryption = (is_production and has_database)

    # Resources
    privateSecurityGroup = ec2.CfnSecurityGroup(self, 'PrivateSecurityGroup',
          group_description = 'Private security group',
          vpc_id = 'vpc-xxxxxxxx',
        )

    publicSecurityGroup = ec2.CfnSecurityGroup(self, 'PublicSecurityGroup',
          group_description = 'Public security group',
          vpc_id = 'vpc-xxxxxxxx',
        )

    myApp = ec2.CfnInstance(self, 'MyApp',
          image_id = regionToAmi['us-east-1']['AMI'],
          tags = [
            {
              'key': 'Name',
              'value': cdk.Fn.select(1, 'My-EC2-Instance'.split('-')),
            },
          ],
          security_groups = [
            privateSecurityGroup.ref if use_private_security_group else publicSecurityGroup.ref,
          ],
        )


