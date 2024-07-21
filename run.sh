#!/bin/bash
#Amazon Linux
# Update the package list
sudo yum update -y

# Install git, python3, and pip3
sudo amazon-linux-extras install epel -y
sudo yum install -y git python3 python3-pip

# Upgrade pip
sudo pip3 install --upgrade pip

# Add cloudflared-ascii.repo to /etc/yum.repos.d/ 
curl -fsSl https://pkg.cloudflare.com/cloudflared-ascii.repo | sudo tee /etc/yum.repos.d/cloudflared-ascii.repo

#update repo
sudo yum update -y

# install cloudflared
sudo yum install cloudflared -y

# sudo yum install -y git
# git clone https://github.com/paniji/comfy-linux.git
# it pull https://github.com/paniji/comfy-linux.git 
# cd comfy-linux
pip3 install -r requirements.txt
sudo cp cpu/svc/flask-app.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl restart flask-app
sudo systemctl enable flask-app
sudo systemctl status flask-app

sudo cp cpu/svc/s3-uploader.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable s3-uploader
sudo systemctl restart s3-uploader
sudo systemctl status s3-uploader

sudo cp cpu/svc/sqs-poller.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl restart sqs-poller
sudo systemctl enable sqs-poller
sudo systemctl status sqs-poller

# ## Prep comfy install
# python3 cpu/prep/comfy.py
# ## Run comfy service
# sudo cp cpu/svc/comfyui.service /etc/systemd/system/
# sudo systemctl daemon-reload
# sudo systemctl restart comfyui
# sudo systemctl enable comfyui
# sudo systemctl status comfyui

# To get more detailed logs for a service managed by systemd, you can use the journalctl command in addition to systemctl status. Here are the steps:

## Check the status of the service:
# sudo systemctl status <service_name>

## Get the logs for the service:
# sudo journalctl -u <service_name>

## Get the most recent logs for the service:
# sudo journalctl -u <service_name> -n 50

## Follow the logs in real-time:
# sudo journalctl -u <service_name> -f

## Get logs for a specific time period:
# sudo journalctl -u <service_name> --since "2023-07-01" --until "2023-07-07"

## Get logs with specific priority:
# sudo journalctl -u <

# curl -X POST http://localhost:5155/prompt -H "Content-Type: application/json" -d '{
#   "6": {
#     "inputs": {
#       "text": "https://cdn.pixabay.com/photo/2017/08/27/20/10/png-2687339_1280.png"
#     }
#   },
#   "9": {
#     "inputs": {
#       "filename_prefix": "pania2--d84d14f2-b5b8-452b-9529-255d4a964fb4_test001"
#     }
#   }
# }'

# curl -X POST http://localhost:5155/prompt -H "Content-Type: application/json" -d '{
#   "3": {
#     "inputs": {
#       "seed": 763007004578560,
#       "steps": 20,
#       "cfg": 8,
#       "sampler_name": "euler",
#       "scheduler": "normal",
#       "denoise": 1,
#       "model": [
#         "4",
#         0
#       ],
#       "positive": [
#         "6",
#         0
#       ],
#       "negative": [
#         "7",
#         0
#       ],
#       "latent_image": [
#         "5",
#         0
#       ]
#     },
#     "class_type": "KSampler",
#     "_meta": {
#       "title": "KSampler"
#     }
#   },
#   "4": {
#     "inputs": {
#       "ckpt_name": "cyberrealisticXL_v11VAE.safetensors"
#     },
#     "class_type": "CheckpointLoaderSimple",
#     "_meta": {
#       "title": "Load Checkpoint"
#     }
#   },
#   "5": {
#     "inputs": {
#       "width": 512,
#       "height": 512,
#       "batch_size": 1
#     },
#     "class_type": "EmptyLatentImage",
#     "_meta": {
#       "title": "Empty Latent Image"
#     }
#   },
#   "6": {
#     "inputs": {
#       "text": "https://cdn.pixabay.com/photo/2017/08/27/20/10/png-2687339_1280.png",
#       "clip": [
#         "4",
#         1
#       ]
#     },
#     "class_type": "CLIPTextEncode",
#     "_meta": {
#       "title": "CLIP Text Encode (Prompt)"
#     }
#   },
#   "7": {
#     "inputs": {
#       "text": "text, watermark",
#       "clip": [
#         "4",
#         1
#       ]
#     },
#     "class_type": "CLIPTextEncode",
#     "_meta": {
#       "title": "CLIP Text Encode (Prompt)"
#     }
#   },
#   "8": {
#     "inputs": {
#       "samples": [
#         "3",
#         0
#       ],
#       "vae": [
#         "4",
#         2
#       ]
#     },
#     "class_type": "VAEDecode",
#     "_meta": {
#       "title": "VAE Decode"
#     }
#   },
#   "9": {
#     "inputs": {
#       "filename_prefix": "pania2--d84d14f2-b5b8-452b-9529-255d4a964fb4_test001",
#       "images": [
#         "8",
#         0
#       ]
#     },
#     "class_type": "SaveImage",
#     "_meta": {
#       "title": "Save Image"
#     }
#   }
# }'

