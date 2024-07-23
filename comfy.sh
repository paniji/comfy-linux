# sudo yum install -y git
# git clone https://github.com/paniji/comfy-linux.git
# it pull https://github.com/paniji/comfy-linux.git 
# cd comfy-linux
python3 cpu/prep/comfy/comfy.py # Comfy Pre 
bash cpu/prep/comfy/init.sh # Cloudflare etc

sudo touch /var/log/comfyui_service.log
sudo chown ec2-user:ec2-user /var/log/comfyui_service.log

# sudo cp cpu/svc/comfy/comfyui.service /etc/systemd/system/
# sudo systemctl daemon-reload
# sudo systemctl start comfyui
# sudo systemctl enable comfyui
# sudo systemctl status comfyui