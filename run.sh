#yum install -y git
#git clone https://github.com/paniji/comfy-linux.git 
#cd comfy-linux
pip3 install -r requirements.txt
sudo mv cpu/svc/flask-app.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl restart flask-app
sudo systemctl enable flask-app
sudo systemctl status flask-app
#curl -X POST http://127.0.0.1:8188/prompt -H "Content-Type: application/json" -d '{"message": "Hello, World!"}'
#curl -X POST http://localhost:8188/prompt -H "Content-Type: application/json" -d '{"path":"https://cdn.pixabay.com/photo/2017/08/27/20/10/png-2687339_1280.png", "key":"d70297a8-e567-42bd-8ed6-7173b2daf30c"}'
sudo mv cpu/svc/s3-uploader.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable s3-uploader
sudo systemctl start s3-uploader
sudo systemctl status s3-uploader


