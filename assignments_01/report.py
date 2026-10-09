from weatherkit.records import to_readings
from weatherkit.summarize import DailyAggregator
import json
from weatherkit import WeatherResponse
with open('weather_raw.json','r') as file:
    data = json.load(file)
    print(data)
weather = WeatherResponse.model_validate(data)
readings = to_readings(weather)
aggregator = DailyAggregator()
summaries = aggregator.summarize(readings)
print(len(summaries))
print(summaries[0])
print(summaries[1])
print(weather.latitude)
print(weather.timezone)
print(len(weather.hourly.time))