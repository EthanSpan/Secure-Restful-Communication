from flask import Flask, request
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import base64
import os
from dotenv import load_dotenv
load_dotenv()

# app secret key and api data definition
app = Flask(__name__)
SECRET_KEY = bytes.fromhex(os.getenv("SECRET_KEY"))
weather_data = {
    "location": "Denton, TX",
    "temperature_celsius": 10,
    "temperature_fahrenheit": 50,
    "condition": "Partly Cloudy",
    "humidity": 61
}

# accepts nonce and uses it with aes gcm for an authentication tag so if its a different nonce the verification will fail
@app.route('/weather')
def display_weather():
    client_nonce = request.args.get('nonce', '')
    if not client_nonce:
        return 'Missing nonce', 400
    plaintext = f'Weather in {weather_data["location"]}: {weather_data["temperature_celsius"]}°C ({weather_data["temperature_fahrenheit"]}°F), {weather_data["condition"]}, Humidity: {weather_data["humidity"]}%'
    aesgcm = AESGCM(SECRET_KEY)
    server_nonce = os.urandom(12)
    aad = client_nonce.encode()
    ciphertext = aesgcm.encrypt(server_nonce, plaintext.encode(), aad)
    payload = server_nonce + ciphertext
    with open('response.bin', 'wb') as f:
        f.write(payload)
    return base64.b64encode(payload).decode()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
