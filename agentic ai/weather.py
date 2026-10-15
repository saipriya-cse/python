
from flask import Flask, request, render_template_string
import urllib.request
import urllib.parse
import json

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>WeatherNow</title>

<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #dbeafe, #818cf8);
    color: #172554;
    min-height: 100vh;
    padding: 30px 15px;
}

.container {
    max-width: 850px;
    margin: auto;
}

header {
    text-align: center;
    margin-bottom: 25px;
}

header h1 {
    font-size: 36px;
    color: #1d4ed8;
    margin-bottom: 8px;
}

header p { color: #475569; }

.search-box, .card, .forecast {
    background: white;
    border-radius: 20px;
    padding: 25px;
    margin-bottom: 20px;
    box-shadow: 0 10px 25px #1e3a8a15;
}

form {
    display: flex;
    gap: 10px;
    margin-top: 20px;
}

input {
    flex: 1;
    min-width: 0;
    padding: 15px;
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    font-size: 16px;
}

button {
    padding: 15px 20px;
    border: none;
    border-radius: 10px;
    background: #2563eb;
    color: white;
    font-size: 15px;
    cursor: pointer;
    font-weight: bold;
}

button:hover { background: #1d4ed8; }

.error {
    background: #fee2e2;
    color: #b91c1c;
    padding: 12px;
    border-radius: 10px;
    margin-top: 15px;
}

.hero {
    background: linear-gradient(120deg, #2563eb, #6366f1);
    color: white;
    border-radius: 20px;
    padding: 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
}

.hero h2 { margin: 0; }

.temp {
    font-size: 65px;
    font-weight: bold;
    margin: 15px 0;
}

.icon { font-size: 75px; }

.grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
    margin-top: 20px;
}

.detail {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 5px 15px #1e3a8a10;
}

.detail p { color: #64748b; }
.detail h3 { margin-bottom: 0; }

.forecast-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    text-align: center;
}

.forecast-grid p { color: #64748b; }

footer {
    text-align: center;
    padding: 20px;
    color: #475569;
    font-size: 13px;
}

@media (max-width: 600px) {
    form { flex-direction: column; }
    .grid { grid-template-columns: repeat(2, 1fr); }
    .forecast-grid { grid-template-columns: repeat(2, 1fr); }
    .hero { padding: 20px; }
    .temp { font-size: 48px; }
    .icon { font-size: 50px; }
}
</style>
</head>

<body>
<div class="container">

<header>
    <h1>🌤️ WeatherNow</h1>
    <p>Your personal weather dashboard</p>
</header>

<section class="search-box">
    <h2>Check the weather</h2>
    <p>Enter any city to see its current weather report.</p>

    <form method="POST">
        <input type="text" name="city"
               placeholder="e.g. Bengaluru, London, Mumbai"
               value="{{ city }}" required>
        <button type="submit">Search Weather</button>
    </form>

    {% if error %}
        <div class="error">{{ error }}</div>
    {% endif %}
</section>

{% if weather %}
<section class="hero">
    <div>
        <p>📍 {{ weather.city }}</p>
        <h2>{{ weather.condition }}</h2>
        <div class="temp">{{ weather.temp }}°C</div>
        <p>Feels like {{ weather.feels }}°C</p>
        <p>Local time: {{ weather.time }}</p>
    </div>
    <div class="icon">{{ weather.icon }}</div>
</section>

<h2>Weather Details</h2>
<section class="grid">
    <div class="detail">
        <p>💧 Humidity</p>
        <h3>{{ weather.humidity }}%</h3>
    </div>
    <div class="detail">
        <p>💨 Wind Speed</p>
        <h3>{{ weather.wind }} km/h</h3>
    </div>
    <div class="detail">
        <p>🌧️ Precipitation</p>
        <h3>{{ weather.rain }} mm</h3>
    </div>
</section>

<h2>Today's Forecast</h2>
<section class="forecast">
    <div class="forecast-grid">
        <div>
            <h3>🌡️ High</h3>
            <p>{{ weather.high }}°C</p>
        </div>
        <div>
            <h3>❄️ Low</h3>
            <p>{{ weather.low }}°C</p>
        </div>
        <div>
            <h3>☔ Rain Chance</h3>
            <p>{{ weather.chance }}%</p>
        </div>
        <div>
            <h3>🌅 Sunrise</h3>
            <p>{{ weather.sunrise }}</p>
        </div>
    </div>
    <p style="text-align:center">🌇 Sunset: {{ weather.sunset }}</p>
</section>
{% endif %}

<footer>Weather data powered by Open-Meteo · Free API</footer>

</div>
</body>
</html>
"""

CODES = {
    0: ("Clear Sky", "☀️"),
    1: ("Mainly Clear", "🌤️"),
    2: ("Partly Cloudy", "⛅"),
    3: ("Overcast", "☁️"),
    45: ("Foggy", "🌫️"),
    48: ("Foggy", "🌫️"),
    51: ("Light Drizzle", "🌦️"),
    53: ("Drizzle", "🌦️"),
    55: ("Heavy Drizzle", "🌧️"),
    61: ("Light Rain", "🌦️"),
    63: ("Moderate Rain", "🌧️"),
    65: ("Heavy Rain", "🌧️"),
    71: ("Light Snow", "🌨️"),
    73: ("Snow", "❄️"),
    75: ("Heavy Snow", "❄️"),
    80: ("Rain Showers", "🌦️"),
    81: ("Rain Showers", "🌧️"),
    82: ("Heavy Showers", "⛈️"),
    95: ("Thunderstorm", "⛈️"),
    96: ("Thunderstorm with Hail", "⛈️"),
    99: ("Severe Thunderstorm", "⛈️")
}


def fetch_json(url):
    req = urllib.request.Request(
        url, headers={"User-Agent": "WeatherNow/1.0"}
    )
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def get_weather(city):
    params = urllib.parse.urlencode({
        "name": city, "count": 1,
        "language": "en", "format": "json"
    })

    geo = fetch_json(
        "https://geocoding-api.open-meteo.com/v1/search?" + params
    )

    places = geo.get("results", [])
    if not places:
        return None, "City not found. Try another city name."

    place = places[0]

    params = urllib.parse.urlencode({
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "current": (
            "temperature_2m,relative_humidity_2m,"
            "apparent_temperature,precipitation,"
            "weather_code,wind_speed_10m"
        ),
        "daily": (
            "temperature_2m_max,temperature_2m_min,"
            "precipitation_probability_max,sunrise,sunset"
        ),
        "timezone": place.get("timezone", "auto"),
        "forecast_days": 1
    })

    data = fetch_json(
        "https://api.open-meteo.com/v1/forecast?" + params
    )

    now = data["current"]
    day = data["daily"]
    condition, icon = CODES.get(
        now["weather_code"], ("Variable Conditions", "🌤️")
    )

    location = ", ".join(
        x for x in [
            place.get("name"),
            place.get("admin1"),
            place.get("country")
        ] if x
    )

    return {
        "city": location,
        "condition": condition,
        "icon": icon,
        "temp": now["temperature_2m"],
        "feels": now["apparent_temperature"],
        "humidity": now["relative_humidity_2m"],
        "wind": now["wind_speed_10m"],
        "rain": now["precipitation"],
        "time": now["time"].replace("T", " "),
        "high": day["temperature_2m_max"][0],
        "low": day["temperature_2m_min"][0],
        "chance": day["precipitation_probability_max"][0],
        "sunrise": day["sunrise"][0].split("T")[-1],
        "sunset": day["sunset"][0].split("T")[-1]
    }, None


@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    error = None
    city = ""

    if request.method == "POST":
        city = request.form.get("city", "").strip()

        if not city:
            error = "Please enter a city name."
        else:
            try:
                weather, error = get_weather(city)
            except Exception:
                error = (
                    "Unable to get weather data. "
                    "Check your internet and try again."
                )

    return render_template_string(
        HTML, weather=weather, error=error, city=city
    )


if __name__ == "__main__":
    app.run(debug=True)

