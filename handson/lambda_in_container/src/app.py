import json

def lambda_handler(event, context):
    print("Incoming event:", json.dumps(event))
    print("Hello, World!")
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Hello, World1!", "input_event" : event})
    }
