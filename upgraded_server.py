from flask import Flask, request
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import secrets

def encrypt_data(data, key):
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  
    ciphertext = aesgcm.encrypt(nonce, data.encode('utf-8'), None)  
    return nonce + ciphertext

with open('secret.key', 'rb') as f:
    server_private_key = serialization.load_pem_private_key(
        f.read(),
        password=None
    )

with open('public.key', 'rb') as f:
    server_public_key = serialization.load_pem_public_key(f.read())

session_key = None

app = Flask(__name__)

weather_data = {
    "location": "Denton, TX",
    "temperature_celsius": 10,
    "temperature_fahrenheit": 50,
    "condition": "Partly Cloudy",
    "humidity": 61,
}

@app.route('/public-key', methods=['GET'])
def get_public_key():
    public_pem = server_public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return public_pem

@app.route('/key-exchange', methods=['POST'])
def receive_data():
    global session_key
    encrypted_key = request.data
    session_key = server_private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return "Received Session Key"

@app.route('/weather')
def display_weather():
    if session_key is None:
        return "No session key", 400
    weather = ""
    for k, v in weather_data.items():
        weather += f"{k},{v}\n"
    encrypted_weather = encrypt_data(weather, session_key)
    return encrypted_weather


if __name__ == '__main__':
    app.run(host='127.0.0.1' ,port=5000, debug=True) 



