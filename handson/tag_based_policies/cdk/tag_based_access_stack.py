from aws_cdk import (
    Stack,
    aws_sns as sns,
    aws_secretsmanager as secretsmanager,
    aws_iam as iam,
    aws_lambda as _lambda,
    Tags,
)
from constructs import Construct

YOUR_PROJECT_NAME = "myprj"

class TagBasedAccessStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Create SNS Topics
        topic_with_tag = sns.Topic(
            self, "TopicWithTag",
            topic_name="topic_with_tag"
        )
        Tags.of(topic_with_tag).add("project_name", YOUR_PROJECT_NAME)

        topic_without_tag = sns.Topic(
            self, "TopicWithoutTag",
            topic_name="topic_without_tag"
        )

        # Create Secrets
        secret_with_tag = secretsmanager.Secret(
            self, "SecretWithTag",
            secret_name="secret_with_tag"
        )
        Tags.of(secret_with_tag).add("project_name", YOUR_PROJECT_NAME)

        secret_without_tag = secretsmanager.Secret(
            self, "SecretWithoutTag",
            secret_name="secret_without_tag"
        )

        # Create IAM Role for Lambda with Tag-Based Policies
        lambda_role = iam.Role(
            self, "LambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            description="Role with tag-based access to SNS and Secrets Manager"
        )

        # Policy for SNS Publish to topics with specific tag
        sns_policy = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["sns:Publish"],
            resources=["*"],
            conditions={
                "StringEquals": {
                    "sns:ResourceTag/project_name": YOUR_PROJECT_NAME
                }
            }
        )

        # Policy for Secrets Manager access to secrets with specific tag
        secrets_policy = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "secretsmanager:GetSecretValue",
                "secretsmanager:DescribeSecret"
            ],
            resources=["*"],
            conditions={
                "StringEquals": {
                    "secretsmanager:ResourceTag/project_name": YOUR_PROJECT_NAME
                }
            }
        )

        # Attach Policies to the Role
        lambda_role.add_to_policy(sns_policy)
        lambda_role.add_to_policy(secrets_policy)

        # Add Basic Execution Role for CloudWatch Logs
        lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSLambdaBasicExecutionRole"
            )
        )

        # Lambda Function Code
        lambda_code = f"""
import json
import boto3

def lambda_handler(event, context):
    output = {{}}
    sns_client = boto3.client('sns')
    secrets_client = boto3.client('secretsmanager')

    # Publish to SNS Topic with Tag
    try:
        sns_client.publish(
            TopicArn='{topic_with_tag.topic_arn}',
            Message='Test message to topic with tag'
        )
        output['sns_topic_with_tag'] = 'ok'
    except Exception as e:
        output['sns_topic_with_tag'] = str(e)

    # Publish to SNS Topic without Tag
    try:
        sns_client.publish(
            TopicArn='{topic_without_tag.topic_arn}',
            Message='Test message to topic without tag'
        )
        output['sns_topic_without_tag'] = 'ok'
    except Exception as e:
        output['sns_topic_without_tag'] = str(e)

    # Read Secret with Tag
    try:
        secrets_client.get_secret_value(
            SecretId='{secret_with_tag.secret_arn}'
        )
        output['secret_with_tag'] = 'ok'
    except Exception as e:
        output['secret_with_tag'] = str(e)

    # Read Secret without Tag
    try:
        secrets_client.get_secret_value(
            SecretId='{secret_without_tag.secret_arn}'
        )
        output['secret_without_tag'] = 'ok'
    except Exception as e:
        output['secret_without_tag'] = str(e)

    print(json.dumps(output))
    return output
"""

        # Create Lambda Function
        test_lambda = _lambda.Function(
            self, "TestLambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="index.lambda_handler",
            code=_lambda.InlineCode(lambda_code),
            role=lambda_role,
            description="Lambda function to test tag-based access to SNS and Secrets Manager"
        )
