# Secure-Restful-Communication

For the functionality of the project we have 3 main dependencies.

Cryptography - Security dependent features library

Requests - http requests

Flask - server handling

To begin running this program the best practice is to make a virtual environment.
Run the commands below to setup the base environment -
```
python3 -m venv .venv
source .venv/bin/activate
pip install flask requests cryptography
```

Now all of the key dependencies for the base environment are in place we need to generate the ca keys, certs, and other keys necessary for this project.

To do this run -
```
python3 keygen.py
python3 keygen_ca.py
python3 cert_key.py
```

Now lets test the basic client and server response.

Run -
```
python3 server.py
# move to a new terminal reinitiate .venv
python3 client.py
```

Now the upgraded version

Run -
```
python3 upgraded_server.py
# move to a new terminal reinitiate .venv
python3 upgraded_client.py
```