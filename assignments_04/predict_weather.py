from weather_model import WeatherClassifier, Prediction
##Task 5##
def main():
    classifier = WeatherClassifier("models/weather_classifier.pkl")
    days = [
{"precipitation_sum": 0,
 "temperature_2m_max": 23,
 "temperature_2m_min": 13,
 "wind_speed_10m_max": 7},

{"precipitation_sum": 15,
 "temperature_2m_max": 4,
 "temperature_2m_min": 0,
 "wind_speed_10m_max": 51},

{"precipitation_sum": 2,
 "temperature_2m_max": 17,
 "temperature_2m_min": 9,
 "wind_speed_10m_max": 22},

{"precipitation_sum": 5,
 "temperature_2m_max": 20,
 "temperature_2m_min": 11,
 "wind_speed_10m_max": 30}
 
 ]
    predictions = classifier.predict(days)
    for day, prediction in zip(days,predictions):
        print(f"Day:{day},Prediction:{prediction.label},Probability:{prediction.probability}")
if __name__ == "__main__":
    main()
#Without having the guard in place,importing predict_weather.py would automatically run the whole weather prediciton program even if the other script only wanted to use one funciton#

#Task 6:Reflection#
# 1. Keeping the features in a fixed order prevents the model
# from confusing one feature with another, like treating
# wind speed as temperature and giving an incorrect prediction.

# 2. Using a tiny practice model makes the tests independent
# of the real saved file. This means the tests can still run
# even if the real file is missing or changes.

# 3. My component is ready because it can accept multiple
# weather records and return predictions. Before production,
# I would add better error handling for invalid weather values.