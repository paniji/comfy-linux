import os
import subprocess

# Options setup
OPTIONS = {
    'UPDATE_COMFY_UI': True,
    'INSTALL_COMFYUI_MANAGER': True,
    'INSTALL_ANIMATEDIFF': True,
    'INSTALL_CUSTOM_NODES_DEPENDENCIES': True
}

# Workspace setup
current_dir = os.getcwd()
AI_WORKSPACE = f"{current_dir}/AI"
COMFY_WORKSPACE = f"{current_dir}/AI/ComfyUI"

os.makedirs(AI_WORKSPACE, exist_ok=True)
os.chdir(AI_WORKSPACE)

if not os.path.isdir(COMFY_WORKSPACE):
    print("-= Initial setup ComfyUI =-")
    subprocess.run(['git', 'clone', 'https://github.com/comfyanonymous/ComfyUI'])

os.chdir(COMFY_WORKSPACE)

if OPTIONS['UPDATE_COMFY_UI']:
    print("-= Updating ComfyUI =-")
    subprocess.run(['git', 'pull'])

print("-= Install dependencies =-")
subprocess.run(['pip', 'install', 'https://download.pytorch.org/whl/cu118/xformers-0.0.22.post4%2Bcu118-cp310-cp310-manylinux2014_x86_64.whl', '-r', 'requirements.txt', '--extra-index-url', 'https://download.pytorch.org/whl/cu121', '--extra-index-url', 'https://download.pytorch.org/whl/cu118', '--extra-index-url', 'https://download.pytorch.org/whl/cu117'])
subprocess.run(['pip', 'install', 'onnxruntime-gpu', 'color-matcher', 'simpleeval'])

if OPTIONS['INSTALL_COMFYUI_MANAGER']:
    os.chdir('custom_nodes')
    if not os.path.isdir('ComfyUI-Manager'):
        print("-= Initial setup ComfyUI-Manager =-")
        subprocess.run(['git', 'clone', 'https://github.com/ltdrdata/ComfyUI-Manager'])
    os.chdir('ComfyUI-Manager')
    subprocess.run(['git', 'pull'])

if OPTIONS['INSTALL_ANIMATEDIFF']:
    os.chdir('../')
    if not os.path.isdir('ComfyUI-AnimateDiff-Evolved'):
        print("-= Initial setup AnimateDiff =-")
        subprocess.run(['git', 'clone', 'https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved'])
    os.chdir('ComfyUI-AnimateDiff-Evolved')
    subprocess.run(['git', 'pull'])

os.chdir(COMFY_WORKSPACE)

if OPTIONS['INSTALL_CUSTOM_NODES_DEPENDENCIES']:
    print("-= Install custom nodes dependencies =-")
    subprocess.run(['python', 'custom_nodes/ComfyUI-Manager/scripts/colab-dependencies.py'])
