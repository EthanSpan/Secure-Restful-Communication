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

Now all of the key dependencies for task 1-4 are in place we need to generate the ca keys, certs, and other keys necessary for this project.

Focusing on task 1,3, and 4 

Change into its respective directory and...

Run -

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
Focusing on task 2 you will need one more dependency so first initiate the venv if necessary and follow the directions in the example.env.md and build your environment.

From here begin testing out the different server cases.

Change into the task2 directory

First we will start with the ae file

Run -

```
python3 server_ae.py
# move to a new terminal reinitiate .venv
python3 client_ae.py
```

Next test the MAC client and server

Run -

```
python3 server_mac.py
# move to a new terminal reinitiate .venv
python3 client_mac.py
```

Next test the fake server using the stolen tag from tag.txt, change the URL in your .env to port 5001

Run -

```
python3 server_mac.py
# move to a new terminal reinitiate .venv
python3 client_mac.py
# stop the mac server, then in the same terminal
python3 server_fake.py
# in the client terminal
python3 client_mac.py
```

Next test the replay attack using the superfake server, response.bin must exist from the ae test above

Run -

```
python3 server_superfake.py
# move to a new terminal reinitiate .venv
python3 client_ae.py
```

Finally test the countermeasure with the updated client and server

Run -

```
python3 server_udp.py
# move to a new terminal reinitiate .venv
python3 client_udp.py
```

To confirm the countermeasure blocks the replay attack

Run -

```
python3 server_superfake.py
# move to a new terminal reinitiate .venv
python3 client_udp.py
```