from weatherkit.records import to_readings
from weatherkit.summarize import DailyAggregator
import json
from weatherkit import WeatherResponse
with open('weather_raw.json','r') as file:
    data = json.load(file)
    print(data)
def main():
    weather = WeatherResponse.model_validate(data)
    readings = to_readings(weather)
    aggregator = DailyAggregator()
    summaries = aggregator.summarize(readings)
    print("Date | High | Low | Precipitation | Temp Range")
    for summary in summaries:
        print(summary.date,
              summary.temp_max,
              summary.temp_min,
              summary.precipitation_sum,
              summary.temp_range()
        )
    incomplete = aggregator.incomplete_days(readings)
    if incomplete:
        print("Warning:Incomplete days dropped:",incomplete)
if __name__ == "__main__":
    main()

## Not having the guard, report.py would run immeditaely if another file imported it.##