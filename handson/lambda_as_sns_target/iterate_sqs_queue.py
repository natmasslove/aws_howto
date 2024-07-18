import boto3
import json

def process_message(message):
    # Parse the message body
    body = json.loads(message['Body'])
    
    # Extract the Subject and Message part
    subject = body.get('Subject')
    message_body = body.get('MessageBody')

    # Print the nicely formatted Subject and Message
    print(f"Subject: {subject}")
    print(f"Message: {json.dumps(json.loads(message_body), indent=2)}")

def main():
    # Create SQS client
    sqs = boto3.client('sqs')

    # get current region and account_id
    region = boto3.session.Session().region_name
    sts = boto3.client('sts')
    account_id = sts.get_caller_identity()["Account"]       

    # Replace with your SQS queue URL
    queue_name = "sqs-sampleam-queue-as-lambda-sink"
    queue_url = f'https://sqs.{region}.amazonaws.com/{account_id}/{queue_name}'

    while True:
        # Receive message from SQS queue
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=10
        )

        messages = response.get('Messages', [])
        if not messages:
            print("No messages in the queue.")
            break

        for message in messages:
            process_message(message)

            # Delete received message from queue
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=message['ReceiptHandle']
            )

if __name__ == "__main__":
    main()
