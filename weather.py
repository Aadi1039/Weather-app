import os
from flask import Flask, render_template, request
import urllib.request
import json

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("WEATHER_API_KEY") 
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric"

def get_weather(city):
    url = BASE_URL.format(city, API_KEY)
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            return {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity']
            }
    except:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    if request.method == "POST":
        city = request.form.get("city")
        weather_data = get_weather(city)
    return render_template("index.html", weather=weather_data)

if __name__ == "__main__":
    app.run(debug=True)
