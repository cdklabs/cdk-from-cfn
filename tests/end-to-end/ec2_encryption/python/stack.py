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
    }

    # Conditions
    has_database = props['databaseType'] == 'mysql'
    is_production = props['environment'] == 'prod'
    use_encryption = (is_production and has_database)

    # Resources
    myApp = ec2.CfnInstance(self, 'MyApp',
          image_id = props['encryptedAmi'] if use_encryption else props['unencryptedAmi'],
        )


