# autogenerated
import aws_cdk as cdk
from stack import EfsStack
app = cdk.App(
    default_stack_synthesizer=cdk.DefaultStackSynthesizer(
        generate_bootstrap_version_rule=False
        )
    )

EfsStack(app, 'Stack')
app.synth()
