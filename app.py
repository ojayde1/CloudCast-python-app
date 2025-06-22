 # app.py
from dotenv import load_dotenv # Import load_dotenv
load_dotenv() # Load environment variables from .env file

#!/usr/bin/env python3
"""
Flask application to fetch and display current weather for any location worldwide.
Uses OpenWeatherMap API.
"""
import requests
from datetime import datetime
from flask import Flask, render_template_string, request
import os # Import the 'os' module

app = Flask(__name__)

# --- IMPORTANT: Read API Key from Environment Variable ---
# For local development, this will be loaded from your .env file.
# In production/CI/CD, it will be provided by the environment (e.g., GitHub Secrets, Kubernetes secrets).
OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")

# HTML template for the web page
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Current Weather</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f4f7f6; color: #333; }
        .container { background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); padding: 30px; text-align: center; }
        h1 { color: #007bff; margin-bottom: 20px; }
        form { margin-bottom: 25px; }
        input[type="text"] { width: 70%; padding: 12px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; margin-right: 10px; }
        button { padding: 12px 25px; background-color: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; transition: background-color 0.3s ease; }
        button:hover { background-color: #0056b3; }
        .weather-info { margin-top: 20px; text-align: left; border-top: 1px solid #eee; padding-top: 20px; }
        .weather-info p { margin: 8px 0; font-size: 18px; line-height: 1.5; }
        .weather-info .label { font-weight: bold; color: #555; display: inline-block; width: 120px; }
        .weather-info .value { color: #007bff; }
        .error { color: #dc3545; font-weight: bold; margin-top: 15px; }
        .footer { margin-top: 30px; font-size: 12px; color: #777; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Current Weather Worldwide</h1>
        <form method="POST" action="/">
            <input type="text" name="location" placeholder="Enter city name (e.g., London, Lagos)" required>
            <button type="submit">Get Weather</button>
        </form>

        {% if error %}
            <p class="error">{{ error }}</p>
        {% elif weather_data %}
            <div class="weather-info">
                <p><span class="label">Location:</span> <span class="value">{{ weather_data.location }}</span></p>
                <p><span class="label">Temperature:</span> <span class="value">{{ "%.1f"|format(weather_data.temp) }}°C</span></p>
                <p><span class="label">Description:</span> <span class="value">{{ weather_data.description }}</span></p>
                <p><span class="label">Humidity:</span> <span class="value">{{ weather_data.humidity }}%</span></p>
                <p><span class="label">Wind Speed:</span> <span class="value">{{ "%.1f"|format(weather_data.wind_speed) }} m/s</span></p>
                <p><span class="label">Last Fetched:</span> <span class="value">{{ weather_data.current_time }}</span></p>
            </div>
        {% endif %}
        <p class="footer">Weather data provided by OpenWeatherMap</p>
    </div>
</body>
</html>
'''

def get_weather_data(location):
    """Fetch current weather data for a given location using OpenWeatherMap API."""
    # Check if API key is set
    if not OPENWEATHER_API_KEY:
        return {'error': "API Key not configured. Please set the OPENWEATHER_API_KEY environment variable."}

    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': location,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric' # Use 'imperial' for Fahrenheit
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            return {
                'location': data['name'],
                'temp': data['main']['temp'],
                'description': data['weather'][0]['description'].capitalize(),
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        else:
            error_message = data.get('message', 'Unknown error').capitalize()
            return {'error': f"Error fetching weather for {location}: {error_message}"}

    except requests.exceptions.RequestException as e:
        return {'error': f"Network error: {e}. Check internet connection or API endpoint."}
    except KeyError as e:
        return {'error': f"Unexpected API response format: Missing key {e}. Please try again."}
    except Exception as e:
        return {'error': f"An unexpected error occurred: {e}"}

@app.route('/', methods=['GET', 'POST'])
def index():
    """Main route to display the weather interface."""
    weather_data = None
    error = None

    # Before handling request, check if API key is generally available
    if not OPENWEATHER_API_KEY:
        error = "OpenWeatherMap API Key is not set in environment variables."
        return render_template_string(HTML_TEMPLATE, error=error)

    if request.method == 'POST':
        location = request.form.get('location')
        if location:
            result = get_weather_data(location)
            if 'error' in result:
                error = result['error']
            else:
                weather_data = result
        else:
            error = "Please enter a location."

    return render_template_string(HTML_TEMPLATE, weather_data=weather_data, error=error)

@app.route('/health')
def health_check():
    """Simple health check endpoint for monitoring."""
    return "OK", 200

if __name__ == "__main__":
    print("Starting web server. Access the weather app at http://127.0.0.1:5000/")
    app.run(host='0.0.0.0', port=5000, debug=True)
