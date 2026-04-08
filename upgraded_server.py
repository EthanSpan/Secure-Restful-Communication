from flask import Flask, request
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import secrets
import json
# as name implies it encrypts the weather data using AES-GCM with the provided key in this instance the session key
def encrypt_data(data, key):
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  
    ciphertext = aesgcm.encrypt(nonce, data.encode('utf-8'), None)  
    return nonce + ciphertext
# grabs the secret key, public key, and certificate for the server
with open('secret.key', 'rb') as f:
    server_private_key = serialization.load_pem_private_key(
        f.read(),
        password=None
    )
with open('public.key', 'rb') as f:
    server_public_key = serialization.load_pem_public_key(f.read())
with open('pk.cert', 'r') as f:
    cert = json.load(f)

# initiates the session key variable, flask app and weather data to be served when requested by the client
session_key = None
app = Flask(__name__)
weather_data = {
    "location": "Denton, TX",
    "temperature_celsius": 10,
    "temperature_fahrenheit": 50,
    "condition": "Partly Cloudy",
    "humidity": 61,
}


# this file initiates a flask server that listens for get requests and serves the weather data when requested
@app.route('/public-key', methods=['GET'])
def get_public_key():
    public_pem = server_public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    response = {
        "public_key": public_pem.hex(),
        "cert": cert
    }
    return json.dumps(response)


# accepts session key from client, decrypts it using the server's private key so the session key can be used later to ensure session is created.
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
# session key is used to encrypt the weather data before it is sent to the client when requested
# if session key is not set then an error message is returned instead
@app.route('/weather')
def display_weather():
    if session_key is None:
        return "No session key", 400
    weather = ""
    for k, v in weather_data.items():
        weather += f"{k},{v}\n"
    encrypted_weather = encrypt_data(weather, session_key)
    return encrypted_weather

# runs server
if __name__ == '__main__':
    app.run(host='127.0.0.1' ,port=5000, debug=True)