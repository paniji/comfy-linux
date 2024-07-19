import os
import subprocess
import threading
import time
import socket
import urllib.request
import platform

# Workspace directory
COMFY_WORKSPACE = "AI/ComfyUI"

# Connecting to Cloudflare
#print("Connecting to Cloudflare...")

#Amazon Linux
# Add cloudflared-ascii.repo to /etc/yum.repos.d/ 
#curl -fsSl https://pkg.cloudflare.com/cloudflared-ascii.repo | sudo tee /etc/yum.repos.d/cloudflared-ascii.repo

#update repo
#sudo yum update

# install cloudflared
#sudo yum install cloudflared -y

# Download and install cloudflared
#cloudflared_url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.rpm"
#if platform.system() == "Linux":
    # Use yum for Amazon Linux 2
    #subprocess.run(["yum", "install", "-y", cloudflared_url])
#else:
    #print("Unsupported operating system")

# Change to the ComfyUI workspace
os.chdir(COMFY_WORKSPACE)

def iframe_thread(port):
    while True:
        time.sleep(0.5)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        if result == 0:
            break
        sock.close()
    print("\nComfyUI finished loading, trying to launch cloudflared (if it gets stuck here cloudflared is having issues)\n")

    p = subprocess.Popen(["cloudflared", "tunnel", "--url", "http://127.0.0.1:{}".format(port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in p.stderr:
        l = line.decode()
        if "trycloudflare.com " in l:
            cf_url = l[l.find("http"):]
            print("This is the URL to access ComfyUI:", cf_url, end='')

# Start a thread to check for the availability of the web server
threading.Thread(target=iframe_thread, daemon=True, args=(8188,)).start()

# Run main.py with the given arguments
subprocess.run(["python", "main.py", "--dont-print-server"])
