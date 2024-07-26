import boto3
import requests
import json
import time
from botocore.exceptions import NoCredentialsError, ClientError

# Constants
SSM_PARAMETER_NAME = "/sqs/cpu-image-queue-url"  # SSM Parameter name for the SQS queue URL
LOCAL_WEB_SERVER_URL = "http://localhost:8188/prompt"
REGION_NAME = "us-east-1"  # AWS region
SQS_POLL_INTERVAL = 5  # Default time in seconds to wait between polling SQS
MAX_SQS_MESSAGES = 50  # Max messages to allow in SQS

def get_region():
    """Fetches the AWS region from environment variables or default configuration."""
    session = boto3.session.Session()
    return session.region_name

# Initialize SSM and SQS clients
region = get_region()
ssm_client = boto3.client('ssm', region_name=REGION_NAME)
sqs_client = boto3.client('sqs', region_name=REGION_NAME)

def get_sqs_queue_url():
    """Fetches the SQS queue URL from SSM Parameter Store."""
    try:
        response = ssm_client.get_parameter(Name=SSM_PARAMETER_NAME)
        return response['Parameter']['Value']
    except (NoCredentialsError, ClientError) as e:
        print(f"SSM error: {e}")
        return None

def get_sqs_queue_length(queue_url):
    """Fetches the current length of the SQS queue."""
    try:
        response = sqs_client.get_queue_attributes(
            QueueUrl=queue_url,
            AttributeNames=['ApproximateNumberOfMessages']
        )
        return int(response['Attributes']['ApproximateNumberOfMessages'])
    except (NoCredentialsError, ClientError) as e:
        print(f"SQS error: {e}")
        return None

def get_comfyui_queue_length():
    """Fetches the number of prompts currently processed by ComfyUI."""
    try:
        response = requests.get(LOCAL_WEB_SERVER_URL)
        if response.status_code == 200:
            data = response.json()
            return data.get("exec_info", {}).get("queue_remaining", 0)
        else:
            print(f"Failed to get queue length from ComfyUI, response code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error fetching queue length from ComfyUI: {e}")
        return None

def poll_sqs_and_process_messages():
    """Polls SQS for messages and processes them."""
    sqs_queue_url = get_sqs_queue_url()
    if not sqs_queue_url:
        print("Failed to retrieve SQS queue URL.")
        return

    while True:
        try:
            # Get the current SQS queue length
            sqs_queue_length = get_sqs_queue_length(sqs_queue_url)
            if sqs_queue_length is None:
                time.sleep(SQS_POLL_INTERVAL)
                continue

            # Check ComfyUI queue length
            comfyui_queue_length = get_comfyui_queue_length()
            if comfyui_queue_length is None:
                time.sleep(SQS_POLL_INTERVAL)
                continue

            # Process messages if ComfyUI is not busy and SQS queue length is above 0
            if comfyui_queue_length == 0 and sqs_queue_length > 0:
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

            # Adjust polling interval based on SQS queue length
            if sqs_queue_length >= MAX_SQS_MESSAGES:
                time.sleep(1)  # Short polling interval if queue is filling up
            else:
                time.sleep(SQS_POLL_INTERVAL)  # Default polling interval

        except (NoCredentialsError, ClientError) as e:
            print(f"SQS error: {e}")

if __name__ == "__main__":
    poll_sqs_and_process_messages()
