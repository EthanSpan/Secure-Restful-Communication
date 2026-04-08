import requests
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
from dotenv import load_dotenv


# shared key and api endpoint definition
load_dotenv()
url = os.getenv("URL")
SECRET_KEY = bytes.fromhex(os.getenv("SECRET_KEY"))


try:
    response = requests.get(url)
    response.raise_for_status()
    raw = base64.b64decode(response.text)
    nonce = raw[:12]
    ciphertext = raw[12:]
    aesgcm = AESGCM(SECRET_KEY)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    print("Successfully Decrypted", plaintext.decode())
except requests.exceptions.RequestException as e:
    print(f'An error occurred: {e}')
except Exception as e:
    print(f'Decryption/authentication failed: {e}')
