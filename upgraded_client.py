from flask import Flask, request
import requests
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

def decrypt_data(encrypted_data, key):
    nonce = encrypted_data[:12]
    ciphertext = encrypted_data[12:]
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode('utf-8')

public_key_url = 'http://127.0.0.1:5000/public-key'
exchange_url = 'http://127.0.0.1:5000/key-exchange'
url = 'http://127.0.0.1:5000/weather'

session_key = os.urandom(32) #generate a random session key

response = requests.get(public_key_url) #get the server's public key
server_public_key = serialization.load_pem_public_key(response.content)
print("Got server public key")

encrypted_session_key = server_public_key.encrypt( #encrypt session key with server's public key
    session_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

requests.post(exchange_url, data=encrypted_session_key) #send encrypted session key to server

try:
    response = requests.get(url)
    response.raise_for_status()
    encrypted_weather = response.content
    decrypted_weather = decrypt_data(encrypted_weather, session_key)
    print("Weather data received and decrypted successfully:")
    print(decrypted_weather)

except requests.exceptions.RequestException as e:
    print(f'An error occurred: {e}')