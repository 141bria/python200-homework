import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

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
counts = df["is_summer"].value_counts()
print(counts)
non_summer_days = counts[0]
summer_days = counts[1]
print("Non-summer days:", non_summer_days)
print("Summer days:",summer_days)
# I do expect is_summer to help predict the daily high becasue summer days are typically warmer than non-summer days.#
#Task 4#

#input#
X = df[["temperature_2m_min"]]
#output#
y= df [["temperature_2m_max"]]
#split the data#
X_train, X_test, y_train,y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state= 42
)
model = LinearRegression()
model.fit(X_train,y_train)
predicted = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test,predicted))
r2 = r2_score(y_test,predicted)
print("Slope:", model.coef_[0])
print("RMSE:",rmse)
print("R2:",r2)
#The RMSE is about 2.90°C, which means a prediciton is off by about 2.90 from the actual temp.#
#Task 5#
feature_cols = ["temperature_2m_min", "precipitation_sum",
                "wind_speed_10m_max", "is_summer"]
X_task5 = df[feature_cols].values
y_task5 = df["temperature_2m_max"].values
X_task5_train, X_task5_test, y_task5_train,y_task5_test = train_test_split(
    X_task5,
    y_task5,
    test_size=0.2,
    random_state=42
)
model_task5 = LinearRegression()
model_task5.fit(X_task5_train,y_task5_train)
predicted_train_task5 = model_task5.predict(X_task5_train)
predicted_task5 = model_task5.predict(X_task5_test)
rmse_task5 = np.sqrt(mean_squared_error(y_task5_test,predicted_task5))
r2_task5 = r2_score(y_task5_test,predicted_task5)
r2_task5_train = r2_score(y_task5_train,predicted_train_task5)
print("R2 Train:",r2_task5_train)
print("RMSE:",rmse_task5)
print("R2 Test:",r2_task5)
for name, coef in zip(feature_cols, model_task5.coef_):
    print(f"{name:22s}: {coef:+.3f}")

# The train and test R² are really close, so the model performs about the same on both.
# Adding the extra features only improved the model a little.
# temperature_2m_min had the biggest positive effect, while precipitation, wind speed, and is_summer lowered the predicted high.
# I was surprised that is_summer was negative because I expected summer days to raise the predicted temperature.

#Task6#
x_task6 = predicted_task5
y_task6 = y_task5_test
low = min(predicted_task5.min(),y_task5_test.min())
high = max(predicted_task5.max(), y_task5_test.max())
plt.scatter(x_task6,y_task6)
plt.plot([low,high],[low,high])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Predicted vs Actual (Full Model)")
plt.savefig("outputs/predicted_vs_actual_high.png")
plt.show()
# The size of the dataset was (366,5) the test size was about 74 since we did 20% for testing. The full model R2 was about 0.909 the full model RMSE was about 2.731C. The largest effect on the module was temperature_2m_min and the direction for the coefficient temperature_2m_min was positive. I was surpised that is_summer was negative because I had expected summer days to increase the predicted high. The RMSE means that the model's predicitons were normalyy off by about 2.73C#