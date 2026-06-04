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
    
    response = requests.post(
        "https://polarremote.com/v2/oauth2/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }
    )
    
    if response.status_code != 200:
        return f"Token alınamadı: {response.text}"
    
    token_data = response.json()
    user_id = token_data.get("x_user_id")
    temp_tokens[user_id] = token_data
    return f"✅ Başarılı! User ID: {user_id}"

@app.route('/polar/metrics/<user_id>')
def get_metrics(user_id):
    token = temp_tokens.get(user_id)
    if not token:
        return jsonify({"error": "user not found"})
    
    response = requests.get(
        "https://www.polaraccesslink.com/v3/users/continuous",
        headers={"Authorization": f"Bearer {token['access_token']}"}
    )
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
