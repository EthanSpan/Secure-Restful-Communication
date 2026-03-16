from flask import Flask

app = Flask(__name__)


weather_data = {
    "location": "Denton, TX",
    "temperature_celsius": 10,
    "temperature_fahrenheit": 50,
    "condition": "Partly Cloudy",
    "humidity": 61
}

@app.route('/weather')
def display_weather():
    return f'Weather in {weather_data["location"]}: {weather_data["temperature_celsius"]}°C ({weather_data["temperature_fahrenheit"]}°F), {weather_data["condition"]}, Humidity: {weather_data["humidity"]}%'


if __name__ == '__main__':
    app.run(host='127.0.0.1' ,port=5000, debug=True) #attempted to use port 5061, but port was blocked and would not allow for a connection so i used port 5000