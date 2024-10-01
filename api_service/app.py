from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

BACKEND_SERVICE_URL = os.getenv('BACKEND_SERVICE_URL', 'http://backend-service.service.local')

@app.route('/messages/greeting', methods=['GET'])
def greeting():
    try:
        response = requests.get(f'{BACKEND_SERVICE_URL}/greeting')
        response.raise_for_status()
        data = response.json()
        return jsonify({"message": data.get('message')}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
