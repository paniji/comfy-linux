import boto3
import json

# Initialize SQS client
sqs_client = boto3.client('sqs', region_name='us-east-1')

# SQS Queue URL
queue_url = 'https://sqs.us-east-1.amazonaws.com/324278473885/CPU-Image-Queue1'

# Base JSON structure
base_json = {
    "6": {
        "inputs": {
            "text": "https://cdn.pixabay.com/photo/2017/08/27/20/10/png-2687339_1280.png"
        }
    },
    "9": {
        "inputs": {
            "filename_prefix": "pania2--d84d14f2-b5b8-452b-9529-255d4a964fb4_test001"
        }
    }
}

# Loop to send 100 messages
for i in range(1, 101):
    # Update the filename_prefix
    base_json["9"]["inputs"]["filename_prefix"] = f"pania2--d84d14f2-b5b8-452b-9529-255d4a964fb4_test{i:03d}"

    # Send message to SQS
    try:
        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(base_json)
        )
        print(f"Message {i} sent successfully: {response['MessageId']}")
    except Exception as e:
        print(f"Failed to send message {i}: {e}")
