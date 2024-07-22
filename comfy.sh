# sudo yum install -y git
# git clone https://github.com/paniji/comfy-linux.git
# it pull https://github.com/paniji/comfy-linux.git 
# cd comfy-linux
python3 cpu/prep/comfy/comfy.py # Comfy Pre 
bash cpu/prep/comfy/init.sh # Cloudflare etc

sudo cp cpu/svc/comfy/comfyui.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl restart comfyui
sudo systemctl enable comfyui
sudo systemctl status comfyui