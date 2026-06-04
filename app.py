from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

CLIENT_ID = "aafde95f-0bee-45c7-86bc-44bad11e8df1"
CLIENT_SECRET = "9879efbb-a5f0-42ce-88cd-c412ac56e8c2"

# Token almak için yeni endpoint (Client Credentials)
@app.route('/polar/token')
def get_token():
    response = requests.post(
        "https://polarremote.com/v2/oauth2/token",
        data={
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }
    )
    if response.status_code != 200:
        return jsonify({"error": "Token alınamadı", "details": response.text}), 400
    return jsonify(response.json())

@app.route('/')
def home():
    return jsonify({"status": "TOAPERFORM Polar API çalışıyor"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
