from flask import Flask
import hmac
import hashlib
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

# returns plaintex api data and hmac tag
@app.route('/weather')
def display_weather():
    plaintext = f'Weather in {weather_data["location"]}: {weather_data["temperature_celsius"]}°C ({weather_data["temperature_fahrenheit"]}°F), {weather_data["condition"]}, Humidity: {weather_data["humidity"]}%'
    tag = hmac.new(SECRET_KEY, plaintext.encode(), hashlib.sha256).hexdigest()
    with open('tag.txt', 'w') as f:
        f.write(tag)
    return f'{plaintext}||{tag}'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
