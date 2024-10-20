

import json

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    request_type = event.get('RequestType', 'UNKNOWN')
    params = event.get('ResourceProperties', {})
    print(f"Request Type: {request_type}")
    print(f"Parameters: {params}")
    return {"statusCode": 200, "body": json.dumps('Function Executed Successfully!')}