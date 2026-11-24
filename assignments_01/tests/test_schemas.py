import json
from pathlib import Path
import pytest
from pydantic import ValidationError
from weatherkit import WeatherResponse
def test_valid_response():
    file_path = Path(__file__).parent.parent/"weather_raw.json"
    with open(file_path,"r",encoding="utf-8") as file:
       data = json.load(file)
    response = WeatherResponse.model_validate(data)
    assert len(response.hourly.time)==168
def test_bad_latitude():
    with pytest.raises(ValidationError):
        bad_data = {
            "longitude": 70.0,
            "latitude":200.0,
            "timezone": "CST",
            "elevation": 99.341,
            "hourly":{"time":["1","3","6","8","9"], 
                      "temperature_2m":[39,49,51,63,72], 
                      "precipitation":[70,34,22,18,3] 
            }
        }
        WeatherResponse.model_validate(bad_data)
def test_mismatched_list():
    with pytest.raises(ValidationError):
        not_a_match = {
            "longitude": 60.0,
            "latitude":70.0,
            "timezone": "CST",
            "elevation": 89.41,
            "hourly":{"time":["1","3","6"], 
                      "temperature_2m":[90,55,53,73,71], 
                      "precipitation":[60,54,32,8,30] 
            }
        }
        WeatherResponse.model_validate(not_a_match)
def test_null_temp():
    with pytest.raises(ValidationError):
        null = {
            "longitude": 50.0,
            "latitude":68.0,
            "timezone": "CST",
            "elevation": 69.41,
            "hourly":{"time":["1","3","6","11","12"], 
                      "temperature_2m":[90,55,None,73,71], 
                      "precipitation":[60,54,32,8,30] 
            }
        }
        WeatherResponse.model_validate(null)
    ##Plain relative paths depend on the folder that you are currently in , but __file__ finds the JSON baased on where it is actually located.##
