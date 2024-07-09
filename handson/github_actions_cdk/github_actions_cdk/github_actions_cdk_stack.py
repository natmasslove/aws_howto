from aws_cdk import (
    # Duration,
    Stack,
    aws_ssm as ssm,
)
from constructs import Construct

class GithubActionsCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        param = ssm.StringParameter(self, "StringParameter",
            parameter_name = 'GitHubActionsParam',
            string_value="value for github actions"
        )