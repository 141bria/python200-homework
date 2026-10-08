from dataclasses import dataclass
from .schemas import WeatherResponse
@dataclass
class HourlyReading:
    """Each HourlyReading will contain the timestamp which is a string, temperature which will be in Celsisus & precipitation in mm
    
    Args:
    response is the validated WeatherResponse which has the hourly weather data

    Returns:
    A list of the HourlyReading
    """
    timestamp : str
    temperature_c : float
    prepcipitation_mm : float
def to_readings(response:WeatherResponse) -> list[HourlyReading]:
    list_of_readings = []
    for reading in zip(response.hourly.time,response.hourly.temperature_2m,response.hourly.precipitation):
        hourly_reading = HourlyReading(*reading)
        list_of_readings.append(hourly_reading)
    return list_of_readings
##HourlyReading is a dataclass instead of Pydantic because it is information we created and trust to be right and clean, WeatherResponse used Pydantic because it was information that we had to check first.###