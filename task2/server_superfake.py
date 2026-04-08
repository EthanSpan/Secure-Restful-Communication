from flask import Flask
import base64

app = Flask(__name__)

# route thats replicating what a replay attack looks like to mediate what this is demonstrating we could do 1 time use or time limits
@app.route('/weather')
def display_weather():
    with open('response.bin', 'rb') as f:
        payload = f.read()
    return base64.b64encode(payload).decode()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
