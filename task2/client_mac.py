import requests
import hmac
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()


# shared key and api endpoint definition
url = os.getenv("URL")
SECRET_KEY = bytes.fromhex(os.getenv("SECRET_KEY"))


# basic request to api for testing using shared key with minor error handling
try:
    response = requests.get(url)
    response.raise_for_status()
    body = response.text
    plaintext, received_tag = body.rsplit('||', 1)
    expected_tag = hmac.new(SECRET_KEY, plaintext.encode(), hashlib.sha256).hexdigest()
    if hmac.compare_digest(expected_tag, received_tag):
        print(f"MAC verified! Api's response: {plaintext}")
    else:
        print("MAC verification failed. The API did not return a response")
except requests.exceptions.RequestException as e:
    print(f'Uh oh an error happened with the server: {e}')
