import os
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
FILES_TO_DOWNLOAD = [
    {
        "path": "AI/ComfyUI/models/checkpoints/wildcardxXLANIMATION.safetensors",
        "url": "https://civitai.com/api/download/models/357959?&token=4304d2c858702a4457d4d46c64e86420"
    },
    {
        "path": "AI/ComfyUI/models/loras/DreamyVibesArtsyle-SDXL-LoRA.safetensors",
        "url": "https://civitai.com/api/download/models/287607?&token=4304d2c858702a4457d4d46c64e86420"
    }
]

def get_region():
    """Fetches the AWS region from environment variables or default configuration."""
    session = boto3.session.Session()
    return session.region_name

def download_files_if_not_exist():
    """Download required files if they do not already exist."""
    for file in FILES_TO_DOWNLOAD:
        if not os.path.exists(file["path"]):
            print(f"Downloading {file['path']} from {file['url']}")
            response = requests.get(file["url"], stream=True)
            if response.status_code == 200:
                os.makedirs(os.path.dirname(file["path"]), exist_ok=True)
                with open(file["path"], "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Downloaded {file['path']}")
            else:
                print(f"Failed to download {file['path']}, status code: {response.status_code}")

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

def queue_prompt(data):
    """Send prompt data to ComfyUI."""
    COMFY = "http://localhost:8188"
    COMFY = os.environ.get('COMFY', COMFY)
    print("Using Comfy URL:", COMFY)
    
    session = requests.Session()
    session.verify = True

    comfy_url = f"{COMFY}/prompt"
    p = {"prompt": data}
    json_data = json.dumps(p).encode('utf-8')

    result = session.post(url=comfy_url, data=json_data)
    
    print("Response Status Code:", result.status_code)
    print("Response Text:", result.text)
    return result.status_code

def poll_sqs_and_process_messages():
    """Polls SQS for messages and processes them."""
    sqs_queue_url = get_sqs_queue_url()
    if not sqs_queue_url:
        print("Failed to retrieve SQS queue URL.")
        return

    # Download required files if they do not exist
    download_files_if_not_exist()

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
                    MaxNumberOfMessages=1,
                    WaitTimeSeconds=10  # Long polling
                )

                messages = response.get('Messages', [])
                for message in messages:
                    message_body = message['Body']
                    receipt_handle = message['ReceiptHandle']

                    try:
                        # Send message to ComfyUI
                        status_code = queue_prompt(json.loads(message_body))
                        if status_code == 200:
                            # Delete message from SQS
                            sqs_client.delete_message(
                                QueueUrl=sqs_queue_url,
                                ReceiptHandle=receipt_handle
                            )
                            print(f"Message {receipt_handle} processed and deleted successfully.")
                        else:
                            print(f"Failed to process message {receipt_handle}, response code: {status_code}")

                    except requests.RequestException as e:
                        print(f"Error sending message to ComfyUI: {e}")

            # Adjust polling interval based on SQS queue length
            if sqs_queue_length >= MAX_SQS_MESSAGES:
                time.sleep(1)  # Short polling interval if queue is filling up
            else:
                time.sleep(SQS_POLL_INTERVAL)  # Default polling interval

        except (NoCredentialsError, ClientError) as e:
            print(f"SQS error: {e}")

if __name__ == "__main__":
    poll_sqs_and_process_messages()
