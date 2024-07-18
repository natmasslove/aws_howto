from aws_cdk import (
    # Duration,
    Stack,
    aws_sns as sns,
    aws_sns_subscriptions as subs,    
    aws_lambda as _lambda,
    aws_sqs as sqs,    
)
from constructs import Construct

class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        topic = sns.Topic(
            self, "SampleSNSTopic",
            display_name="sns-sampleam-topic-with-lambda-target",
            topic_name="sns-sampleam-topic-with-lambda-target"
        )

        # Create an SQS queue
        queue = sqs.Queue(
            self, "SampleSQSQueue",
            queue_name="sqs-sampleam-queue-as-lambda-sink"
        )

        # Create a Lambda function
        lambda_function = _lambda.Function(
            self, "MyFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            function_name="lambda-sampleam-function",
            handler="index.handler",
            code=_lambda.Code.from_inline(
                """
import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
sqs = boto3.client('sqs')

def handler(event, context):
    logger.info(f"event = {event}")
    queue_url = '""" + queue.queue_url + """'
    for record in event['Records']:
        sns_data = record['Sns']
        message_id = sns_data.get('MessageId','N/A')
        message_body = sns_data.get('Message','Message body is not found')
        subject = sns_data.get('Subject','No subject')
        message = {
            'Id': message_id,
            'Subject': subject,
            'MessageBody': message_body
        }
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message)
        )
    return {"statusCode": 200, "body": json.dumps('Success')}
                """
            )
        )

        # Grant the Lambda function permissions to send messages to the SQS queue
        queue.grant_send_messages(lambda_function)

        # Add the Lambda function as a subscription to the SNS topic
        topic.add_subscription(subs.LambdaSubscription(lambda_function))        