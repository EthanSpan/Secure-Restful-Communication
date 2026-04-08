from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# rsa public and private key generation based on the cryptography library similar to keygen
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

# create info for CA private then public key below in PEM format
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
# inserts to appropriate files specifically for CA keys
with open('public_ca.key', 'wb') as f:
    f.write(public_pem)
with open('secret_ca.key', 'wb') as f:
    f.write(private_pem)