import os
import boto3
import requests
import time
from botocore.exceptions import NoCredentialsError

# Define constants
COMFY_WORKSPACE = "AI/ComfyUI/Output"
S3_BUCKET_NAME = "autosynth-image-324278473885-us-east-1-dev"  # Replace with your S3 bucket name
SQS_SERVICE_URL = "http://localhost:5160/start_polling"  # URL to trigger the SQS polling service

# Initialize S3 client
s3_client = boto3.client('s3')

def upload_file_to_s3(file_path, bucket_name, key):
    """Uploads a file to an S3 bucket."""
    try:
        s3_client.upload_file(file_path, bucket_name, key)
        print(f"File {file_path} uploaded to S3 bucket {bucket_name} with key {key}")
        return True
    except NoCredentialsError:
        print("Credentials not available")
        return False
    except Exception as e:
        print(f"Failed to upload {file_path} to S3: {str(e)}")
        return False

def signal_sqs_service():
    """Signals the SQS service to poll immediately."""
    try:
        response = requests.post(SQS_SERVICE_URL)
        if response.status_code == 200:
            print("Successfully signaled SQS service to start polling.")
        else:
            print(f"Failed to signal SQS service, response code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error signaling SQS service: {e}")

def main():
    """Main function to continuously check the workspace and upload files to S3."""
    while True:
        try:
            for filename in os.listdir(COMFY_WORKSPACE):
                file_path = os.path.join(COMFY_WORKSPACE, filename)
                key = filename

                if upload_file_to_s3(file_path, S3_BUCKET_NAME, key):
                    os.remove(file_path)
                    print(f"File {file_path} removed after upload")
                    signal_sqs_service()  # Signal the SQS service to poll immediately
                else:
                    print(f"Failed to upload {file_path}, will retry later")

        except Exception as e:
            print(f"An error occurred: {str(e)}")

        time.sleep(3)  # Check every 60 seconds

if __name__ == "__main__":
    main()
