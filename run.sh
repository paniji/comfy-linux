#yum install -y git
#git clone https://github.com/paniji/comfy-linux.git 
#cd comfy-linux
pip3 install -r requirements.txt
sudo mv cpu/svc/flask-app.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start flask-app
sudo systemctl enable flask-app
sudo systemctl status flask-app
curl -X POST http://127.0.0.1:8188/prompt -H "Content-Type: application/json" -d '{"message": "Hello, World!"}'


