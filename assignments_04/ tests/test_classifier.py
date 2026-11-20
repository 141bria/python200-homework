#Task 4#
import pytest
from weather_model.classifier import WeatherClassifier,Prediction
import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

@pytest.fixture
def tiny_model(tmp_path):
    df = pd.DataFrame([
   {"precipitation_sum":0,
    "temperature_2m_max":23,
    "temperature_2m_min":13,
    "wind_speed_10m_max": 7},
    {"precipitation_sum":15,
    "temperature_2m_max":4,
    "temperature_2m_min":0,
    "wind_speed_10m_max": 51},
    {"precipitation_sum":10.9 ,
    "temperature_2m_max":27,
    "temperature_2m_min":6,
    "wind_speed_10m_max":60}
    ])
    labels = [1,0,0]
    pipe = Pipeline([
        ('scaler',StandardScaler()),
        ('classifier',LogisticRegression())
    ])
    pipe.fit(df,labels)
    joblib.dump(pipe,tmp_path / "tiny_model.pkl")
    return WeatherClassifier(tmp_path / "tiny_model.pkl")
def test_predictions(tiny_model):
    days = [{"precipitation_sum":0,
        "temperature_2m_max":23,
        "temperature_2m_min":13,
        "wind_speed_10m_max": 7},
        {"precipitation_sum":15,
        "temperature_2m_max":4,
        "temperature_2m_min":0,
        "wind_speed_10m_max": 51},
        {"precipitation_sum":10.9 ,
        "temperature_2m_max":27,
        "temperature_2m_min":6,
        "wind_speed_10m_max":60}]
    predictions = tiny_model.predict(days)
    assert len(predictions)==3
    assert all(isinstance(p, Prediction) for p in predictions)
    assert all(0 <= p.probability <= 1 for p in predictions)
def test_empty_list(tiny_model):
    assert tiny_model.predict([]) == []
def test_missing_feature(tiny_model):
    with pytest.raises(ValueError,match="missing feature"):
        tiny_model.predict([{
            "temperature_2m_max":27,
            "temperature_2m_min":6,
            "wind_speed_10m_max":60}])
def test_missing_file(tiny_model):
    with pytest.raises(FileNotFoundError,match="Model file was not found"):
        WeatherClassifier("fake_model.pkl")
@pytest.mark.parametrize("day,expected_label",[
        ({"precipitation_sum": 0,
      "temperature_2m_max": 23,
      "temperature_2m_min": 13,
      "wind_speed_10m_max": 7}, "good"),
      ({"precipitation_sum": 15,
      "temperature_2m_max": 4,
      "temperature_2m_min": 0,
      "wind_speed_10m_max": 51}, "skip")
        ])
def test_weather_labels(tiny_model,day,expected_label):
    predictions = tiny_model.predict([day])
    assert predictions[0].label == expected_label


#test_weather_labels caught the change from "good" to "skip"#
