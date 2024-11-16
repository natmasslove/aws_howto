from aws_cdk import (
    Stack,
    aws_ssm as ssm,
    CfnOutput,
)
from constructs import Construct


class ExecRoleDemoStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Create an SSM Parameter
        ssm_parameter = ssm.StringParameter(
            self, "SSMParameter",
            parameter_name="/demo/parameter",
            string_value="This is a demo parameter",
            description="A demo SSM parameter for the stack"
        )

        CfnOutput(
            self, "ParameterArnOutput",
            value=ssm_parameter.parameter_arn,
            description="The ARN of the SSM Parameter"
        )