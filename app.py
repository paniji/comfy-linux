import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Define the workspace directory
COMFY_WORKSPACE = "AI/ComfyUI/Output"

@app.route('/prompt', methods=['POST'])
def handle_prompt():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    try:
        # Extract path and key from the new JSON structure
        path = data["6"]["inputs"]["text"]
        key = data["9"]["inputs"]["filename_prefix"] #.split("--")[1]
    except KeyError as e:
        return jsonify({"error": f"Missing key in JSON data: {str(e)}"}), 400

    try:
        # Download the PNG file
        response = requests.get(path)
        response.raise_for_status()  # Check for HTTP request errors
        
        # Create the workspace directory if it doesn't exist
        os.makedirs(COMFY_WORKSPACE, exist_ok=True)
        
        # Define the file path to save the image
        file_path = os.path.join(COMFY_WORKSPACE, f"{key}.png")
        
        # Save the image to the specified path
        with open(file_path, 'wb') as file:
            file.write(response.content)
        
        return jsonify({"message": f"File saved as {file_path}"}), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to download the image: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5155)
