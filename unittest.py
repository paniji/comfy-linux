import os
import requests
import json

def queue_prompt(data):
    # Default Comfy URL
    COMFY = "http://localhost:8188"
    
    # Get the value of the 'COMFY' environment variable if it exists
    COMFY = os.environ.get('COMFY', COMFY)
    print("Using Comfy URL:", COMFY)

    # Setup session
    session = requests.Session()
    session.verify = True

    # Define the URL for the prompt endpoint
    comfy_url = f"{COMFY}/prompt"

    # Wrap the data in a dictionary with a key "prompt"
    p = {"prompt": data}

    # Convert the data to JSON-encoded string and then to UTF-8 bytes
    json_data = json.dumps(p).encode('utf-8')

    # Post the JSON data to the ComfyUI prompt endpoint
    #headers = {'Content-Type': 'application/json'}
    result = session.post(url=comfy_url, data=json_data)
    
    # Print the result of the POST request
    print("Response Status Code:", result.status_code)
    print("Response Text:", result.text)

# JSON data
data = {
    "3": {
        "inputs": {
            "seed": 309605814563920,
            "steps": 20,
            "cfg": 8,
            "sampler_name": "euler",
            "scheduler": "normal",
            "denoise": 1,
            "model": [
                "10",
                0
            ],
            "positive": [
                "6",
                0
            ],
            "negative": [
                "7",
                0
            ],
            "latent_image": [
                "5",
                0
            ]
        },
        "class_type": "KSampler",
        "_meta": {
            "title": "KSampler"
        }
    },
    "4": {
        "inputs": {
            "ckpt_name": "wildcardxXLANIMATION.safetensors"
        },
        "class_type": "CheckpointLoaderSimple",
        "_meta": {
            "title": "Load Checkpoint"
        }
    },
    "5": {
        "inputs": {
            "width": 512,
            "height": 512,
            "batch_size": 1
        },
        "class_type": "EmptyLatentImage",
        "_meta": {
            "title": "Empty Latent Image"
        }
    },
    "6": {
        "inputs": {
            "text": "beautiful scenery nature glass bottle landscape, , purple galaxy bottle,",
            "clip": [
                "10",
                1
            ]
        },
        "class_type": "CLIPTextEncode",
        "_meta": {
            "title": "CLIP Text Encode (Prompt)"
        }
    },
    "7": {
        "inputs": {
            "text": "text, watermark",
            "clip": [
                "10",
                1
            ]
        },
        "class_type": "CLIPTextEncode",
        "_meta": {
            "title": "CLIP Text Encode (Prompt)"
        }
    },
    "8": {
        "inputs": {
            "samples": [
                "3",
                0
            ],
            "vae": [
                "4",
                2
            ]
        },
        "class_type": "VAEDecode",
        "_meta": {
            "title": "VAE Decode"
        }
    },
    "9": {
        "inputs": {
            "filename_prefix": "ComfyUI",
            "images": [
                "8",
                0
            ]
        },
        "class_type": "SaveImage",
        "_meta": {
            "title": "Save Image"
        }
    },
    "10": {
        "inputs": {
            "lora_name": "DreamyVibesArtsyle-SDXL-LoRA.safetensors",
            "strength_model": 1,
            "strength_clip": 1,
            "model": [
                "4",
                0
            ],
            "clip": [
                "4",
                1
            ]
        },
        "class_type": "LoraLoader",
        "_meta": {
            "title": "Load LoRA"
        }
    }
}

# Queue the prompt
queue_prompt(data)
