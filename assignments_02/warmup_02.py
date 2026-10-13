import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
                #The scikit-learn API#
#Q1#
rng = np.random.default_rng(42)
temp_min = np.array([1,4,8,12,16,20]).reshape(-1,1)
temp_max = np.array([8,10,15,18,23,27])

model = LinearRegression() #Step 1 create
model.fit(temp_min,temp_max) #Step 2 fit
predicted = model.predict(temp_min) #Step 3 predict

print("Slope:",model.coef_[0])
print("Intercept:",model.intercept_)

plt.scatter(temp_min,temp_max,color="blue",alpha=0.5,label="Data")
plt.plot(temp_min,predicted,color="red",label="Linear fit")
plt.xlabel("Daily low (C)")
plt.ylabel("Daily high (C)")
plt.legend()
new_predictions = (model.predict([
    [6],
    [18]
]))
print("Prediction for low of 6:",new_predictions[0])
print("Prediction for low of 18:",new_predictions[1])
plt.show()

#Q2#
x = np.array([10,20,30,40,50])
print(x.shape)
x_2d = x.reshape(-1,1)
print(x_2d.shape)
# X needs to be 2D so scikit-learn can tell which values are samples and which are features.#

                        #Linear Regression#
rng = np.random.default_rng(42)
num_days  = 120
temp_min  = rng.uniform(-5, 22, num_days)
is_rainy  = rng.integers(0, 2, num_days).astype(float)
temp_max  = 1.0 * temp_min + 6 - 4 * is_rainy + rng.normal(0, 2, num_days)

#Q1#
plt.scatter(temp_min,temp_max,c=is_rainy,cmap="coolwarm",alpha=0.5)
plt.title("Daily High vs Low")
plt.xlabel("temp_min")
plt.ylabel("temp_max")
plt.savefig("outputs/high_vs_low.png")
plt.show
# The rainy days and the dry days show two groups, rainy days usually have lower high temps than dry days with similar low temps, so is_rainy may be helpful for predicting the temp max.#
#Q2#
X = temp_min.reshape(-1,1)
y = temp_max
X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size=0.2,
                                                    random_state=42)
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)
#Q3#
model_1= LinearRegression()
model_1.fit(X_train,y_train)
predicted_1= model_1.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test,predicted_1))
r2 = r2_score(y_test,predicted_1)

print("Slope:",model_1.coef_[0])
print("Intercept:",model_1.intercept_)
print("RMSE:",rmse)
print("R2:",r2)
#As the daily low temp gets higher the daily high temp as geta higher.#
#Q4#
X_full = np.column_stack([temp_min, is_rainy])
model_2 = LinearRegression()
## AI assistance was used to help me understand why the updated two-feature data needed to be split again.##
X_train_2,X_test_2,y_train_2,y_test_2 = train_test_split(
    X_full,
    y,
    test_size= 0.2,
    random_state=42
)
model_2.fit(X_train_2,y_train_2)
predicted_2 = model_2.predict(X_test_2)
rmse = np.sqrt(mean_squared_error(y_test_2,predicted_2))
r2 = r2_score(y_test_2,predicted_2)
#stopping point#