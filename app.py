from flask import Flask, render_template, request, jsonify
from utils import decrypt_data, encrypt_data
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "Stream Overlay Generator - Ready"

@app.route('/overlay')
def overlay():
    data_bundle = request.args.get('data')
    stream_key = request.args.get('key')
    
    if not data_bundle or not stream_key:
        return "Missing data or key", 400
    
    decrypted_json = decrypt_data(data_bundle, stream_key)
    if not decrypted_json:
        return "Invalid key or data", 403
    
    try:
        config = json.loads(decrypted_json)
    except json.JSONDecodeError:
        return "Corrupt data", 400
    
    return render_template('overlay.html', config=config)

@app.route('/generate', methods=['POST'])
def generate():
    # Helper endpoint to generate the encrypted URL
    req_data = request.json
    stream_key = req_data.get('key')
    payload = req_data.get('payload') # This would be a JSON string of overlay settings
    
    if not stream_key or not payload:
        return jsonify({"error": "Missing key or payload"}), 400
    
    encrypted_payload = encrypt_data(payload, stream_key)
    return jsonify({
        "encrypted_payload": encrypted_payload,
        "overlay_url": f"/overlay?data={encrypted_payload}&key={stream_key}"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
