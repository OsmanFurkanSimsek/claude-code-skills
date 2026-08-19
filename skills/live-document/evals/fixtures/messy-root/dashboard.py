"""weather-dashboard: one-page Flask app with cached Open-Meteo data."""
import json
import time
from pathlib import Path

import requests
from flask import Flask, jsonify, render_template

app = Flask(__name__)

CACHE_DIR = Path(__file__).parent / "cache"
CACHE_TTL_SECONDS = 3600
LATITUDE, LONGITUDE = 39.93, 32.86  # Ankara
API_URL = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={LATITUDE}&longitude={LONGITUDE}"
    "&current_weather=true&hourly=temperature_2m,precipitation"
    "&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
)


def fetch_forecast() -> dict:
    """Return forecast JSON, served from the file cache while it is fresh."""
    CACHE_DIR.mkdir(exist_ok=True)
    cache_file = CACHE_DIR / "forecast.json"
    if cache_file.exists() and time.time() - cache_file.stat().st_mtime < CACHE_TTL_SECONDS:
        return json.loads(cache_file.read_text())
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    data = response.json()
    cache_file.write_text(json.dumps(data))
    return data


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/forecast")
def forecast():
    try:
        return jsonify(fetch_forecast())
    except requests.RequestException:
        stale = CACHE_DIR / "forecast.json"
        if stale.exists():
            return jsonify(json.loads(stale.read_text()))
        return jsonify({"error": "upstream unavailable"}), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
