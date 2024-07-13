from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/prompt', methods=['POST'])
def handle_prompt():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    # Process the JSON data here
    # For demonstration, let's just return the received JSON
    return jsonify(data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8188)
