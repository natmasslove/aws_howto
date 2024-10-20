import json

from aws_cdk import (
    CustomResource,
    Stack,
    Fn,
    aws_iam as iam,
    aws_lambda as _lambda,
    custom_resources as cr,
)
from constructs import Construct


class LambdaInvokeStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Define the Lambda function
        lambda_function = _lambda.Function(
            self,
            "MyLambdaFunction",
            function_name="lambda-test-invoke",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="lambda_sample.lambda_handler",
            code=_lambda.Code.from_asset("src/"),
        )

        provider = cr.Provider(self, "my-provider", on_event_handler=lambda_function)

        CustomResource(
            self,
            "my-cr",
            service_token=provider.service_token,
            properties={"SampleParameter": "Hello from CDK", "ListParameter": ["aa", "bc"]},
        )
