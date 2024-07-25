# sudo yum install -y git
# git clone https://github.com/paniji/comfy-linux.git
# it pull https://github.com/paniji/comfy-linux.git 
# cd comfy-linux

source activate pytorch

pip install einops
pip install torchsde
pip install aiohttp
pip install kornia
pip install spandrel

python3 cpu/prep/comfy/comfy.py # Comfy Pre 
bash cpu/prep/comfy/init.sh # Cloudflare etc

wget -O AI/ComfyUI/models/checkpoints/wildcardxXLANIMATION.safetensors "https://civitai.com/api/download/models/357959?&token=4304d2c858702a4457d4d46c64e86420"
wget -O AI/ComfyUI/models/loras/DreamyVibesArtsyle-SDXL-LoRA.safetensors "https://civitai.com/api/download/models/287607?&token=4304d2c858702a4457d4d46c64e86420"

# sudo touch /var/log/comfyui_service.log
# sudo chown ec2-user:ec2-user /var/log/comfyui_service.log

## For ComfyUI service
# sudo cp cpu/svc/comfy/comfyui.service /etc/systemd/system/
# sudo systemctl daemon-reload
# sudo systemctl start comfyui
# sudo systemctl enable comfyui
# sudo systemctl status comfyui

## For UI access
# python3 server.py