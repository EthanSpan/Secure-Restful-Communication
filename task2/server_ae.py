from flask import Flask
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
SECRET_KEY = bytes.fromhex(os.getenv("SECRET_KEY"))
weather_data = {
    "location": "Denton, TX",
    "temperature_celsius": 10,
    "temperature_fahrenheit": 50,
    "condition": "Partly Cloudy",
    "humidity": 61
}

# route that returns an encrypted payload using aes gcm
@app.route('/weather')
def display_weather():
    plaintext = f'Weather in {weather_data["location"]}: {weather_data["temperature_celsius"]}°C ({weather_data["temperature_fahrenheit"]}°F), {weather_data["condition"]}, Humidity: {weather_data["humidity"]}%'
    aesgcm = AESGCM(SECRET_KEY)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)
    payload = nonce + ciphertext
    with open('response.bin', 'wb') as f:
        f.write(payload)
    return base64.b64encode(payload).decode()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
