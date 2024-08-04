import os
import requests
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

# Constants
SSM_MODELS_PARAMETER_NAME = os.environ.get('SSM_MODELS_PARAMETER_NAME')  # SSM Parameter name for the models list
REGION_NAME = "us-east-1"  # AWS region

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

def download_file_http(url, file_path):
    """Downloads a file from an HTTP(S) URL."""
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Downloaded {file_path} from {url}")
        else:
            print(f"Failed to download {file_path} from {url}, status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error downloading {file_path} from {url}: {e}")

def download_file_s3(url, file_path):
    """Downloads a file from an S3 URL."""
    s3_client = boto3.client('s3')
    try:
        bucket_name, key = parse_s3_url(url)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        s3_client.download_file(bucket_name, key, file_path)
        print(f"Downloaded {file_path} from {url}")
    except (NoCredentialsError, ClientError) as e:
        print(f"Error downloading {file_path} from {url}: {e}")

def parse_s3_url(url):
    """Parses an S3 URL and returns the bucket name and key."""
    url_parts = url.replace("s3://", "").split("/")
    bucket_name = url_parts.pop(0)
    key = "/".join(url_parts)
    return bucket_name, key

def download_files_if_not_exist():
    """Download required files if they do not already exist."""
    files_to_download = get_files_to_download()
    if not files_to_download:
        print("Failed to retrieve files to download from SSM.")
        return

    for file in files_to_download:
        if not os.path.exists(file["path"]):
            url = file["url"]
            if url.startswith("http://") or url.startswith("https://"):
                download_file_http(url, file["path"])
            elif url.startswith("s3://"):
                download_file_s3(url, file["path"])
            else:
                print(f"Unsupported URL scheme for {url}")

if __name__ == "__main__":
    download_files_if_not_exist()
