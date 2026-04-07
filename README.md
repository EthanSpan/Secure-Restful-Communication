# Secure-Restful-Communication


Task 3:
For the following files upgraded_client, upgraded_server, and the keygen file. The purpose of these files is to establish an initial connection through the exchange of a public key which allows for the exchange of a private session key. After the exchange takes place aesgcm is used to provide authenticated encryption to ensure tampering of message is difficult.

For the upgraded client and server file simply run the keygen file using the following command
python3 keygen.py

then run the server file 
python3 upgraded_server.py

lastly run the client file 
python3 upgraded_server.py