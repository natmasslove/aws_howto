# Using Lambda as a target for SNS topic

This how-to is to showcase how to
1. Create SNS topic, Lambda function and SQS queue using AWS CDK
2. Lambda is a receipient for SNS topic and publishes messages as-is to SQS queue
3. A Python script which reads all messages from SQS queue