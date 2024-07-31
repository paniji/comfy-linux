import os
import requests

FILES_TO_DOWNLOAD = [
    {
        "path": "/home/ec2-user/comfy-linux/AI/ComfyUI/models/checkpoints/wildcardxXLANIMATION.safetensors",
        "url": "https://civitai.com/api/download/models/357959?&token=4304d2c858702a4457d4d46c64e86420"
    },
    {
        "path": "/home/ec2-user/comfy-linux/AI/ComfyUI/models/loras/DreamyVibesArtsyle-SDXL-LoRA.safetensors",
        "url": "https://civitai.com/api/download/models/287607?&token=4304d2c858702a4457d4d46c64e86420"
    }
]

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

if __name__ == "__main__":
    download_files_if_not_exist()
