# Explanation
# S3 Uploader Service:

# Signals the SQS service immediately upon detecting a file in the workspace.
# Uploads the file to S3 and removes it from the local directory after a successful upload.
# SQS Service:

# Checks for the signal file before polling SQS.
# Polls immediately if the signal file is present, otherwise uses the default poll interval.
# Processes and deletes messages from the SQS queue after successful processing.
# This setup should ensure that the SQS service polls for new messages as soon as a file is detected by the S3 uploader service, 
# without waiting for the upload to complete.

import boto3
import requests
import json
import time
import os
from botocore.exceptions import NoCredentialsError, ClientError

# Constants
SSM_PARAMETER_NAME = "/sqs/cpu-image-queue-url"  # SSM Parameter name for the SQS queue URL
DEFAULT_SQS_POLL_INTERVAL = 10  # Default time in seconds to wait between polling SQS
SIGNAL_FILE_PATH = "/tmp/sqs_poll_signal"  # Path to the signal file
LOCAL_WEB_SERVER_URL = "http://localhost:5155/prompt"

def get_region():
    """Fetches the AWS region from environment variables or default configuration."""
    session = boto3.session.Session()
    return session.region_name

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

    while True:
        try:
            # Check for signal file to determine if we should poll immediately
            if os.path.exists(SIGNAL_FILE_PATH):
                os.remove(SIGNAL_FILE_PATH)
                poll_interval = 0  # Poll immediately
            else:
                poll_interval = DEFAULT_SQS_POLL_INTERVAL

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

        time.sleep(poll_interval)

if __name__ == "__main__":
    poll_sqs_and_process_messages()



# import boto3
# import requests
# import json
# import time
# from botocore.exceptions import NoCredentialsError, ClientError

# # Constants
# SSM_PARAMETER_NAME = "/sqs/cpu-image-queue-url"  # SSM Parameter name for the SQS queue URL
# SQS_POLL_INTERVAL = 10  # Time in seconds to wait between polling SQS
# LOCAL_WEB_SERVER_URL = "http://localhost:5155/prompt"

# def get_region():
#     """Fetches the AWS region from environment variables or default configuration."""
#     session = boto3.session.Session()
#     return session.region_name

# # Initialize SSM and SQS clients
# region = get_region()
# ssm_client = boto3.client('ssm', region_name='us-east-1')
# sqs_client = boto3.client('sqs', region_name='us-east-1')

# def get_sqs_queue_url():
#     """Fetches the SQS queue URL from SSM Parameter Store."""
#     try:
#         response = ssm_client.get_parameter(Name=SSM_PARAMETER_NAME)
#         return response['Parameter']['Value']
#     except (NoCredentialsError, ClientError) as e:
#         print(f"SSM error: {e}")
#         return None

# def poll_sqs_and_process_messages():
#     """Polls SQS for messages and processes them."""
#     sqs_queue_url = get_sqs_queue_url()
#     if not sqs_queue_url:
#         print("Failed to retrieve SQS queue URL.")
#         return

#     while True:
#         try:
#             response = sqs_client.receive_message(
#                 QueueUrl=sqs_queue_url,
#                 MaxNumberOfMessages=1,  # Adjust based on your needs
#                 WaitTimeSeconds=10  # Long polling
#             )

#             messages = response.get('Messages', [])
#             for message in messages:
#                 message_body = message['Body']
#                 receipt_handle = message['ReceiptHandle']

#                 try:
#                     # Send message to local web server
#                     resp = requests.post(LOCAL_WEB_SERVER_URL, json=json.loads(message_body))
#                     if resp.status_code == 200:
#                         # Delete message from SQS
#                         sqs_client.delete_message(
#                             QueueUrl=sqs_queue_url,
#                             ReceiptHandle=receipt_handle
#                         )
#                         print(f"Message {receipt_handle} processed and deleted successfully.")
#                     else:
#                         print(f"Failed to process message {receipt_handle}, response code: {resp.status_code}")

#                 except requests.RequestException as e:
#                     print(f"Error sending message to local web server: {e}")

#         except (NoCredentialsError, ClientError) as e:
#             print(f"SQS error: {e}")

#         time.sleep(SQS_POLL_INTERVAL)

# if __name__ == "__main__":
#     poll_sqs_and_process_messages()
