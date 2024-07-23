import os
import subprocess
import threading
import time
import socket
import logging

# Configure logging
logging.basicConfig(filename='/var/log/comfyui_service.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Workspace directory
COMFY_WORKSPACE = "AI/ComfyUI"

# Change to the ComfyUI workspace
os.chdir(COMFY_WORKSPACE)

def iframe_thread(port):
    while True:
        try:
            time.sleep(0.5)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', port))
            if result == 0:
                break
            sock.close()
        except Exception as e:
            logging.error(f"Error in iframe_thread: {e}")
    
    logging.info("ComfyUI finished loading, trying to launch cloudflared")
    
    # try:
    #     p = subprocess.Popen(["cloudflared", "tunnel", "--url", "http://127.0.0.1:{}".format(port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #     for line in p.stderr:
    #         l = line.decode()
    #         if "trycloudflare.com " in l:
    #             cf_url = l[l.find("http"):]
    #             logging.info(f"This is the URL to access ComfyUI: {cf_url}")
    # except Exception as e:
    #     logging.error(f"Error launching cloudflared: {e}")

# Start a thread to check for the availability of the web server
threading.Thread(target=iframe_thread, daemon=True, args=(8188,)).start()

try:
    # Run main.py with the given arguments
    subprocess.run(["python3", "main.py", "--dont-print-server"])
except Exception as e:
    logging.error(f"Error running main.py: {e}")

# import os
# import subprocess
# import threading
# import time
# import socket

# # Options setup
# OPTIONS = {
#     'USE_CLOUDFLARE': True
# }

# # Workspace setup
# current_dir = os.getcwd()
# COMFY_WORKSPACE = f"{current_dir}/AI/ComfyUI"

# os.chdir(COMFY_WORKSPACE)

# def iframe_thread(port):
#     while True:
#         time.sleep(0.5)
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         result = sock.connect_ex(('127.0.0.1', port))
#         if result == 0:
#             break
#         sock.close()

# # Start a thread to check for the availability of the web server
# port = 8188
# threading.Thread(target=iframe_thread, daemon=True, args=(port,)).start()

# # Run main.py with the given arguments
# subprocess.run(["python3", "main.py", "--dont-print-server"])

# # Cloudflare integration
# if OPTIONS['USE_CLOUDFLARE']:
#     print("\nComfyUI finished loading, trying to launch cloudflared (if it gets stuck here cloudflared is having issues)\n")
#     p = subprocess.Popen(["cloudflared", "tunnel", "--url", f"http://127.0.0.1:{port}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     for line in p.stderr:
#         l = line.decode()
#         if "trycloudflare.com " in l:
#             cf_url = l[l.find("http"):]
#             print("This is the URL to access ComfyUI:", cf_url, end='')
