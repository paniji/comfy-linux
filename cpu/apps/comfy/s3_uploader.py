import os
import time
import boto3
from botocore.exceptions import NoCredentialsError

# Define constants
COMFY_WORKSPACE = "AI/ComfyUI/output"
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

def main():
    """Main function to continuously check the workspace and upload files to S3."""
    while True:
        try:
            for filename in os.listdir(COMFY_WORKSPACE):
                if filename.endswith(".png"):  # Adjust the condition if you want to upload other file types
                    file_path = os.path.join(COMFY_WORKSPACE, filename)
                    key = filename
                    
                    if upload_file_to_s3(file_path, S3_BUCKET_NAME, key):
                        os.remove(file_path)
                        print(f"File {file_path} removed after upload")
                    else:
                        print(f"Failed to upload {file_path}, will retry later")
                    
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        time.sleep(60)  # Check every 60 seconds

if __name__ == "__main__":
    main()
