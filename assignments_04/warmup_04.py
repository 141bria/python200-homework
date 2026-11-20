                            #Warmup#
#Q1#
import json
from dataclasses import dataclass
import pytest
class ModelInfo:
    def __init__(self,path):
        with open(path,"r") as file:
            self.data = json.load(file)
    def feature_count(self)-> int:
        return len(self.data["features"])
data = {"features":["temperature_2m_max","wind_speed_10m_max"]}
with open ("list_of_features.json","w") as file:
    json.dump(data,file)
info = ModelInfo("list_of_features.json")
print(info.feature_count())
# Loading the file once in __init__ is faster becasue feature_count can reuse the data instead of reopening the file everytime it's called.#
#Q2#
@dataclass
class DayForecast:
    date: str
    high_c: float
    will_rain: bool
    def summary(self)->str:
        if self.will_rain:
            rain= "rain is expected"
        else:
            rain = "rain is not expected"
        return f"{self.date}: high {self.high_c}C,{rain}" 
forecast_1= DayForecast("2026-07-04",23.5,True)
forecast_2= DayForecast("2025-09-03",31,False)
print(forecast_1.summary())
print(forecast_2.summary())
#The dataclass automatically created __init__ for me so I didn't have to write it myself.#
#Q3#
def parse_temperature(text:str)-> float:
    try:
        float(text)
    except ValueError: 
        raise ValueError(f"You can't change {text} to a temperature!")
    return float(text)
def test_parse_temperature_valid():
    assert parse_temperature("24.1")== pytest.approx(24.1)
def test_parse_temperature_bad_input_raises():
    with pytest.raises(ValueError, match="temperature"):
        parse_temperature("hot")
#pytest.raises(ValueError) would catch the error but without match it doesn't check to see if the message has "temperature".#