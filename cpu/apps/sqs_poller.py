import boto3
import requests
import json
from flask import Flask, request, jsonify
from botocore.exceptions import NoCredentialsError, ClientError

# Constants
SSM_PARAMETER_NAME = "/sqs/cpu-image-queue-url"  # SSM Parameter name for the SQS queue URL
LOCAL_WEB_SERVER_URL = "http://localhost:5155/prompt"

def get_region():
    """Fetches the AWS region from environment variables or default configuration."""
    session = boto3.session.Session()
    return session.region_name

# Initialize Flask app
app = Flask(__name__)

# Initialize SSM and SQS clients
region = get_region()
ssm_client = boto3.client('ssm', region_name='us-east-1')
sqs_client = boto3.client('sqs', region_name='us-east-1')

def get_sqs_queue_url():
    """Fetches the SQS queue URL from SSM Parameter Store."""
    try:
        response = ssm_client.get_parameter(Name=SSM_PARAMETER_NAME)
        return response['Parameter']['Value']
    except (NoCredentialsError, ClientError) as e:
        print(f"SSM error: {e}")
        return None

def poll_sqs_and_process_messages():
    """Polls SQS for messages and processes them."""
    sqs_queue_url = get_sqs_queue_url()
    if not sqs_queue_url:
        print("Failed to retrieve SQS queue URL.")
        return

    try:
        response = sqs_client.receive_message(
            QueueUrl=sqs_queue_url,
            MaxNumberOfMessages=1,  # Adjust based on your needs
            WaitTimeSeconds=10  # Long polling
        )

        messages = response.get('Messages', [])
        for message in messages:
            message_body = message['Body']
            receipt_handle = message['ReceiptHandle']

            try:
                # Send message to local web server
                resp = requests.post(LOCAL_WEB_SERVER_URL, json=json.loads(message_body))
                if resp.status_code == 200:
                    # Delete message from SQS
                    sqs_client.delete_message(
                        QueueUrl=sqs_queue_url,
                        ReceiptHandle=receipt_handle
                    )
                    print(f"Message {receipt_handle} processed and deleted successfully.")
                else:
                    print(f"Failed to process message {receipt_handle}, response code: {resp.status_code}")

            except requests.RequestException as e:
                print(f"Error sending message to local web server: {e}")

    except (NoCredentialsError, ClientError) as e:
        print(f"SQS error: {e}")

@app.route('/start_polling', methods=['POST'])
def start_polling():
    """Endpoint to start polling SQS."""
    poll_sqs_and_process_messages()
    return jsonify({"message": "SQS polling triggered successfully"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5160)
