import requests
import base64
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
from dotenv import load_dotenv
load_dotenv()

# app secret key and api data definition
SECRET_KEY = bytes.fromhex(os.getenv("SECRET_KEY"))
url = os.getenv("URL")

# uses fresh nonce every request and sends the nonce in the url parameter.
try:
    client_nonce = base64.b64encode(os.urandom(16)).decode()
    response = requests.get(url, params={'nonce': client_nonce})
    response.raise_for_status()
    raw = base64.b64decode(response.text)
    server_nonce = raw[:12]
    ciphertext = raw[12:]
    aesgcm = AESGCM(SECRET_KEY)
    aad = client_nonce.encode()
    plaintext = aesgcm.decrypt(server_nonce, ciphertext, aad)
    print(plaintext.decode())

except requests.exceptions.RequestException as e:
    print(f'An error occurred: {e}')
except Exception as e:
    print(f'Decryption/authentication failed: {e}')
