import os
import time
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

# Define constants
COMFY_WORKSPACE = "AI/ComfyUI/output"
SSM_PARAMETER_NAME = "/s3image/bucket_name"  # SSM Parameter name for the S3 bucket name
REGION_NAME = "us-east-1"  # AWS region

# Initialize S3 and SSM clients
s3_client = boto3.client('s3')
ssm_client = boto3.client('ssm', region_name=REGION_NAME)

def get_ssm_parameter(name):
    """Fetches the value of an SSM parameter."""
    try:
        response = ssm_client.get_parameter(Name=name)
        return response['Parameter']['Value']
    except (NoCredentialsError, ClientError) as e:
        print(f"SSM error: {e}")
        return None

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

def main():
    """Main function to continuously check the workspace and upload files to S3."""
    s3_bucket_name = get_ssm_parameter(SSM_PARAMETER_NAME)
    if not s3_bucket_name:
        print("Failed to retrieve S3 bucket name from SSM.")
        return

    while True:
        try:
            for filename in os.listdir(COMFY_WORKSPACE):
                if filename.endswith(".png"):  # Adjust the condition if you want to upload other file types
                    file_path = os.path.join(COMFY_WORKSPACE, filename)
                    key = filename
                    
                    if upload_file_to_s3(file_path, s3_bucket_name, key):
                        os.remove(file_path)
                        print(f"File {file_path} removed after upload")
                    else:
                        print(f"Failed to upload {file_path}, will retry later")
                    
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        time.sleep(2)  # Check every 60 seconds

if __name__ == "__main__":
    main()
