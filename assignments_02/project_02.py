import requests
import pandas as pd
import matplotlib.pyplot as plt

#Task 1#
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": 35.15,
    "longitude": -90.05,
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "daily": [
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_sum",
        "wind_speed_10m_max",
    ],
    "timezone": "America/Chicago",
}
response = requests.get(url,params=params)
response.raise_for_status()
df = pd.DataFrame(response.json()["daily"])
df["date"] = pd.to_datetime(df["time"])
df = df.drop("time",axis=1)
print(df.shape)
print(df.head(5))
#I chose Memphis,TN.#

#Task 2#
print(df.describe())
#There were no missing values.#
print(df.corr(numeric_only=True)["temperature_2m_max"].sort_values())
#The temperature_2m_min correlates the strongest with temperature_2m_max.#
x = df["temperature_2m_min"]
y = df["temperature_2m_max"]
plt.scatter(x,y)
plt.title("Correlation between temp_min vs temp_max")
plt.xlabel("temp_min")
plt.ylabel("temp_max")
plt.savefig("outputs/correlation_tempmin_tempmax.png")
plt.show()
#As the min temp increases, the max temp also increases which shows the strong positive correlation between them.#
#Task3#
summer_months = [6,7,8]
df["is_summer"] = df["date"].dt.month.isin(summer_months).astype(int)