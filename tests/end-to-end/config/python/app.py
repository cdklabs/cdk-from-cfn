# autogenerated
import aws_cdk as cdk
from stack import ConfigStack
app = cdk.App(
    default_stack_synthesizer=cdk.DefaultStackSynthesizer(
        generate_bootstrap_version_rule=False
        )
    )

ConfigStack(app, 'Stack')
app.synth()