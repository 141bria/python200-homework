from pydantic import BaseModel, Field, model_validator
class HourlyBlock (BaseModel):
    """Class that tracks the time, temperature, and precipitation each hour"""
    time:list [str]
    temperature_2m : list[float]
    precipitation : list[float]
    @model_validator(mode="after")
    def wrong_length(self):
        if len(self.time) != len(self.temperature_2m) or len (self.precipitation) != len(self.time):
            raise ValueError("All list should be the same length!")
        return self
    

class WeatherResponse (BaseModel):
    """class that gets the latitude, longitude, timezone, elevation each hour."""
    latitude : float = Field(ge=-90,le=90)
    longitude : float = Field(ge=-180,le=180)
    timezone : str
    elevation : float
    hourly: HourlyBlock