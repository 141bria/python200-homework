from weatherkit import WeatherResponse
from weatherkit.records import to_readings, HourlyReading
weather_data= {
"latitude": 33.333,
"longitude": 77.9311,
"timezone": "EST",
"elevation": 80.222,
"hourly":{
    "time":["3","1","7"],
"temperature_2m":[14,1,2],
"precipitation":[4,40,67]
}
}
def test_readings_order():
    weather = WeatherResponse.model_validate(weather_data)
    readings = to_readings(weather)
    assert len(readings) == 3
    assert readings[0].timestamp== "3"
    assert readings[-1].timestamp == "7"
def test_readings_match_input():
    weather = WeatherResponse.model_validate(weather_data)
    readings = to_readings(weather)
    assert readings[1].timestamp == weather_data["hourly"]["time"][1]
    assert readings[1].temperature_c == weather_data["hourly"]["temperature_2m"][1]
    assert readings[1].prepcipitation_mm == weather_data["hourly"]["precipitation"][1]
def test_identical_objects():
    first_reading = HourlyReading("1am",72,25)
    second_reading = HourlyReading("1am",72,25)
    assert first_reading == second_reading