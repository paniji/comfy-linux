import os
import time
import boto3
from botocore.exceptions import NoCredentialsError

# Define constants
COMFY_WORKSPACE = "AI/ComfyUI/Output"
S3_BUCKET_NAME = "autosynth-image-324278473885-us-east-1-dev"  # Replace with your S3 bucket name

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

def upload_directory_to_s3(local_directory, bucket_name, s3_prefix=''):
    """Uploads a directory and its contents to an S3 bucket."""
    for root, dirs, files in os.walk(local_directory):
        for filename in files:
            local_path = os.path.join(root, filename)
            relative_path = os.path.relpath(local_path, local_directory)
            s3_path = os.path.join(s3_prefix, relative_path)

            if upload_file_to_s3(local_path, bucket_name, s3_path):
                os.remove(local_path)
                print(f"File {local_path} removed after upload")
            else:
                print(f"Failed to upload {local_path}, will retry later")

        for dir in dirs:
            dir_path = os.path.join(root, dir)
            s3_path = os.path.join(s3_prefix, os.path.relpath(dir_path, local_directory))
            s3_client.put_object(Bucket=bucket_name, Key=s3_path + '/')

def main():
    """Main function to continuously check the workspace and upload files to S3."""
    while True:
        try:
            if os.path.exists(COMFY_WORKSPACE):
                upload_directory_to_s3(COMFY_WORKSPACE, S3_BUCKET_NAME)

        except Exception as e:
            print(f"An error occurred: {str(e)}")

        time.sleep(60)  # Check every 60 seconds

if __name__ == "__main__":
    main()
