import json
from assignments_01.weatherkit import WeatherResponse
with open('weather_raw.json','r') as file:
    data = json.load(file)
    print(data)
weather = WeatherResponse.model_validate(data)
print(weather.latitude)
print(weather.timezone)
print(len(weather.hourly.time))