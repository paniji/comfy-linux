import os
import subprocess
import threading
import time
import socket

def iframe_thread(port):
    while True:
        time.sleep(0.5)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        if result == 0:
            break
        sock.close()
    print("\nComfyUI service is running, launching Cloudflare tunnel...\n")

    p = subprocess.Popen(["cloudflared", "tunnel", "--url", "http://127.0.0.1:{}".format(port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in p.stderr:
        l = line.decode()
        if "trycloudflare.com " in l:
            cf_url = l[l.find("http"):]
            print("This is the URL to access ComfyUI:", cf_url, end='')

# Start a thread to check for the availability of the ComfyUI service
threading.Thread(target=iframe_thread, daemon=True, args=(8188,)).start()

# Keep the script running
while True:
    time.sleep(60)
