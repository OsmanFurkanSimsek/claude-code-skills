# scratch: poking at the Open-Meteo response shape before wiring it into dashboard.py
import requests

url = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=39.93&longitude=32.86&hourly=temperature_2m&timezone=auto"
)
data = requests.get(url, timeout=10).json()
print(list(data.keys()))
print(data["hourly"]["time"][:5])
print(data["hourly"]["temperature_2m"][:5])
