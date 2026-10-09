import json
from pathlib import Path
import pytest
from pydantic import ValidationError
from weatherkit import WeatherResponse
def test_valid_response(filepath):
    file_path = Path(__file__).parent.parent/"weather_raw.json"
    with open("weather_raw.json","r",encoding="utf-8") as file:
        content = file.read