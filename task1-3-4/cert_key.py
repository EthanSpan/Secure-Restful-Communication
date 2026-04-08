import json
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

# opening the files used for pk cert creation
with open('public.key', 'rb') as f:
    server_public_pem = f.read()

with open('secret_ca.key', 'rb') as f:
    ca_private_key = serialization.load_pem_private_key(f.read(), password=None)

# provides message tp be encoded in the certificate
key_hex = server_public_pem.hex()
message = f"This public key: {key_hex} belongs to hjs0100"

# creates info for public key certificate by signing the message with CA's private key using PSS padding and SHA256 hashing
signature = ca_private_key.sign(
    message.encode('utf-8'),
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

cert = {
    "message": message,
    "signature": signature.hex()
}

with open('pk.cert', 'w') as f:
    json.dump(cert, f)