# sudo yum install -y git
# git clone https://github.com/paniji/comfy-linux.git
# it pull https://github.com/paniji/comfy-linux.git 
# cd comfy-linux

source activate pytorch

pip3 install -r requirements.txt

pip install einops
pip install torchsde
pip install aiohttp
pip install kornia
pip install spandrel

python3 cpu/prep/comfy/comfy.py # Comfy Pre 
bash cpu/prep/comfy/init.sh # Cloudflare etc

wget -O AI/ComfyUI/models/checkpoints/wildcardxXLANIMATION.safetensors "https://civitai.com/api/download/models/357959?&token=4304d2c858702a4457d4d46c64e86420"
wget -O AI/ComfyUI/models/loras/DreamyVibesArtsyle-SDXL-LoRA.safetensors "https://civitai.com/api/download/models/287607?&token=4304d2c858702a4457d4d46c64e86420"

python3 --version
python3 -m pip install --upgrade pip
python3 -m venv myenv
source myenv/bin/activate
pip install boto3
pip install requests
deactivate

sudo cp cpu/svc/comfy/s3-uploader.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable s3-uploader
sudo systemctl start s3-uploader
sudo systemctl status s3-uploader

sudo cp cpu/svc/comfy/sqs-poller.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start sqs-poller
sudo systemctl enable sqs-poller
sudo systemctl status sqs-poller

# # ComfyUI service
sudo cp cpu/svc/comfy/comfyui.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start comfyui
sudo systemctl enable comfyui
sudo systemctl status comfyui

## Upgrade python if needed for boto3 compatibility.. sometime python worl it out and fix lines below before the services
# cd /usr/src
# sudo wget https://www.python.org/ftp/python/3.11.4/Python-3.11.4.tgz
# sudo tar xzf Python-3.11.4.tgz
# cd Python-3.11.4
# sudo ./configure --enable-optimizations
# sudo make altinstall
# python3.11 --version

# python3.11 -m pip install --upgrade pip
# python3.11 -m venv myenv
# source myenv/bin/activate
# pip install boto3
# pip install requests

# python3 
# python3 -m pip install --upgrade pip
# python3 -m venv myenv
# source myenv/bin/activate
# pip install boto3
# pip install requests
# deactivate

# # ComfyUI service
# sudo cp cpu/svc/comfy/comfyui.service /etc/systemd/system/
# sudo systemctl daemon-reload
# sudo systemctl start comfyui
# sudo systemctl enable comfyui
# sudo systemctl status comfyui

# # S3 Uploader service
# sudo cp cpu/svc/comfy/s3-uploader.service /etc/systemd/system/
# sudo systemctl daemon-reload
# sudo systemctl enable s3-uploader
# sudo systemctl start s3-uploader
# sudo systemctl status s3-uploader

# # SQS Poller service
# sudo cp cpu/svc/comfy/sqs-poller.service /etc/systemd/system/
# sudo systemctl daemon-reload
# sudo systemctl start sqs-poller
# sudo systemctl enable sqs-poller
# sudo systemctl status sqs-poller

## For UI access
# source activate pytorch
# python3 server.py