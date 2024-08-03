import os
import boto3
import requests
import json
import time
from botocore.exceptions import NoCredentialsError, ClientError

# Constants
SSM_PARAMETER_NAME = "/sqs/cpu-image-queue-url"  # SSM Parameter name for the SQS queue URL
SSM_MODELS_PARAMETER_NAME = "/sqs/cpu-image-queue1-models"  # SSM Parameter name for the models list
LOCAL_WEB_SERVER_URL = "http://localhost:8188/prompt"
REGION_NAME = "us-east-1"  # AWS region
SQS_POLL_INTERVAL = 2  # Default time in seconds to wait between polling SQS
MAX_SQS_MESSAGES = 50  # Max messages to allow in SQS

def get_ssm_parameter(name):
    """Fetches the value of an SSM parameter."""
    ssm_client = boto3.client('ssm', region_name=REGION_NAME)
    try:
        response = ssm_client.get_parameter(Name=name)
        return response['Parameter']['Value']
    except (NoCredentialsError, ClientError) as e:
        print(f"SSM error: {e}")
        return None

def get_ssm_parameter_list(name):
    """Fetches the value of an SSM StringList parameter."""
    ssm_client = boto3.client('ssm', region_name=REGION_NAME)
    try:
        response = ssm_client.get_parameter(Name=name)
        return response['Parameter']['Value'].split(',')
    except (NoCredentialsError, ClientError) as e:
        print(f"SSM error: {e}")
        return None

def get_files_to_download():
    """Fetches the list of files to download from SSM Parameter Store."""
    file_names = get_ssm_parameter_list(SSM_MODELS_PARAMETER_NAME)
    files_to_download = []
    
    for file_name in file_names:
        path = get_ssm_parameter(f"/comfy-ui/{file_name}/path")
        url = get_ssm_parameter(f"/comfy-ui/{file_name}/url")
        if path and url:
            files_to_download.append({"path": path, "url": url})
    
    return files_to_download

def check_models_exist(files_to_download):
    """Check if required files already exist."""
    for file in files_to_download:
        if not os.path.exists(file["path"]):
            return False
    return True

def get_sqs_queue_url():
    """Fetches the SQS queue URL from SSM Parameter Store."""
    return get_ssm_parameter(SSM_PARAMETER_NAME)

def get_sqs_queue_length(queue_url):
    """Fetches the current length of the SQS queue."""
    sqs_client = boto3.client('sqs', region_name=REGION_NAME)
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

    # Get files to download from SSM parameter store
    files_to_download = get_files_to_download()
    if not files_to_download:
        print("Failed to retrieve files to download from SSM.")
        return

    # Check if required models are downloaded
    while not check_models_exist(files_to_download):
        print("Models are not downloaded yet. Waiting...")
        time.sleep(5)  # Wait for 10 seconds before checking again

    sqs_client = boto3.client('sqs', region_name=REGION_NAME)
    
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
