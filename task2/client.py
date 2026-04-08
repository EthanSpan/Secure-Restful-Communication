import requests

url = 'http://127.0.0.1:5000/weather'

try:
    response = requests.get(url)
    response.raise_for_status()  
    print(response.text)  

except requests.exceptions.RequestException as e:
    print(f'An error occurred: {e}')