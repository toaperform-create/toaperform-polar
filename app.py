from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

CLIENT_ID = "a5d151bb-5a0a-4538-8d5b-23e35bd756e4"
CLIENT_SECRET = "155b0449-fa85-49d9-835a-2d64fb8d2a77"
REDIRECT_URI = "https://polar-api.onrender.com/polar/callback"

temp_tokens = {}

@app.route('/')
def home():
    return jsonify({"status": "TOAPERFORM Polar API çalışıyor"})

@app.route('/polar/auth-url')
def auth_url():
    url = f"https://flow.polar.com/oauth2/authorization?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
    return jsonify({"auth_url": url})

@app.route('/polar/callback')
def polar_callback():
    code = request.args.get('code')
    if not code:
        return "code gerekli"
    return f"Callback alındı. Kod: {code}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
