#yum install -y git
#git clone https://github.com/paniji/comfy-linux.git
#git pull https://github.com/paniji/comfy-linux.git 
#cd comfy-linux
pip3 install -r requirements.txt
sudo cp cpu/svc/flask-app.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl restart flask-app
sudo systemctl enable flask-app
sudo systemctl status flask-app
#curl -X POST http://127.0.0.1:8188/prompt -H "Content-Type: application/json" -d '{"message": "Hello, World!"}'
#curl -X POST http://localhost:8188/prompt -H "Content-Type: application/json" -d '{"path":"https://cdn.pixabay.com/photo/2017/08/27/20/10/png-2687339_1280.png", "key":"d70297a8-e567-42bd-8ed6-7173b2daf30c"}'
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

# curl -X POST http://localhost:8188/prompt -H "Content-Type: application/json" -d '{
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
#       "filename_prefix": "pania2--d70297a8-e567-42bd-8ed6-7173b2daf30c",
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

