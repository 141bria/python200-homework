from dataclasses import dataclass
import joblib
from pathlib import Path
import pandas as pd
#Task 1#
@dataclass
class Prediction:
    """will have good or skip"""
    label : str
    """the probability from 0-1"""
    probability : float

#Task 2#
"""Loads a saved weather model and predicts running conditions"""
class WeatherClassifier:
    """Loads the saved weather model.
    Raises:
    FileNotFoundError: If the model file is missing.
    """
    def __init__(self,model_path:str|Path) ->None:
        file_path = Path(model_path)
        if not file_path.exists():
            raise FileNotFoundError (f"Model file was not found:{file_path}")
        else:
            self.model = joblib.load(file_path)
    def predict(self,days:list[dict[str,float]])->list[Prediction]:
        """Predicts whether each day is good for running.
    Raises:
    ValueError:If a requried weather feature is missing."""
        FEATURES = ["precipitation_sum",
    "temperature_2m_max",
    "temperature_2m_min",
    "wind_speed_10m_max"]
        if not days:
            return []
        for day in days:
            for feature in FEATURES:
                if feature not in day:
                    raise ValueError(f"missing feature: {feature}")
        weather_days = pd.DataFrame(days)
        weather_days[FEATURES]
        running_days = self.model.predict(weather_days[FEATURES])
        probabilities = self.model.predict_proba(weather_days[FEATURES])[:,1]
        predictions = []
        for result, probability in zip(running_days,probabilities):
            if result == 1:
               label = "good"
            else:
                label="skip"
            predictions.append(Prediction(label,float(probability)))
        return predictions
# AI Assistance Disclosure:
# I used AI for guidance on Python syntax, indentation,
# debugging, and understanding assignment instructions.
# ChatGPT also provided some code examples and helped me
# correct specific sections while I worked through the assignment.