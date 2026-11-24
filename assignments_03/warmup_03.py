import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, ConfusionMatrixDisplay, classification_report,
)
import joblib

df = pd.read_csv("weather_classification.csv")
numeric = ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "wind_speed_10m_max"]
X = df[numeric]
y = df["good_for_running"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
                                    #Preprocessing#
#Q1#
scaler = StandardScaler()
X_trained_scaled = scaler.fit_transform(X_train)
X_transformed = scaler.transform(X_test)
mean_x_train = sum(X_trained_scaled)/len(X_trained_scaled)
print(mean_x_train)
# We gave the scaler the test set only becasue we don't our numbers to be influenced by the test set, by not doing this we prevent the model from indireectly seeig it and helps us get the right measure of how the model would perform on new data.#

#Q2#
encoder = OneHotEncoder(sparse_output=False)
seasons = [["winter"],["spring"],["summer"],["fall"]]
encoded = encoder.fit_transform(seasons)
print(encoder.get_feature_names_out())
print(encoded.shape)
#The single season column became a total of four columns. It broke down into four because it had four categories.#
#Q3#
categorical_features = ["season"]
numeric_features = ["temperature_2m_max",
"temperature_2m_min",
"precipitation_sum",
"wind_speed_10m_max"
]
new_features = numeric_features + ["season"]
added_feature = df[new_features]
X_train, X_test, y_train,y_test = train_test_split(
    added_feature,
    y,test_size=0.2,
    random_state=42,
    stratify=y
)
preprocess = ColumnTransformer(
    transformers = [
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"),categorical_features),
    ]
)
model = Pipeline(
    steps = [
        ("preprocess",preprocess),
        ("classifier",LogisticRegression(max_iter=1000))
    ]
)
model.fit(X_train,y_train)
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test,predictions)
print(accuracy)
#The pipeline will automatically preprocess the data and then it would run the model vs me doing that by hand.#
                    #KNN#
#Q1#
knn_scaled = Pipeline([
    ("scaler",StandardScaler()),
    ("knn",KNeighborsClassifier(n_neighbors=5)),
])
numeric = ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "wind_speed_10m_max"]
X = df[numeric]
y = df["good_for_running"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
knn_scaled.fit(X_train,y_train)
y_pred = knn_scaled.predict(X_test) # AI assisted me with getting this line of code to get the predictions using the trained KNN model.#
print("Scaled accuracy:", accuracy_score(y_test,knn_scaled.predict(X_test)))
print(classification_report(y_test,y_pred,target_names=["skip","good"]))

#Q2#
for k in [1, 3, 5, 7, 9, 11, 15, 21]:
    knn = Pipeline([
        ("scaler", StandardScaler()),
        ("knn",KNeighborsClassifier(n_neighbors=k)),
    ])
    scores = cross_val_score(knn,X_train,y_train, cv=7)
    print(f"K={k:5d}: mean={scores.mean():.3f} std={scores.std():.3f}")
    #I would chose the K value of 9 because it has a higher mean and a low standard deviation.#
#Q3#
knn_unscaled = KNeighborsClassifier(n_neighbors=5)
knn_unscaled.fit(X_train,y_train)
print("Unscaled accuracy:", accuracy_score(y_test,knn_unscaled.predict(X_test)))
knn_scaled1 = KNeighborsClassifier(n_neighbors=5)
knn_scaled1.fit(X_train,y_train)
print("Scaled accuracy:", accuracy_score(y_test,knn_scaled1.predict(X_test)))
#No, scaling didn't help in this case. However scaling would be vital to use for a distance based model so if something is greater in distance than another feature it isn't weighed more than what it should be.#
                    #Logistic Regression#
#Q1#
model = Pipeline([
    ("scaler",StandardScaler()),
    ("logreg",LogisticRegression(max_iter=1000)),
])
model.fit(X_train,y_train)
y_pred1=model.predict(X_test)
print(classification_report(y_test,y_pred,target_names=["skip","good"]))
#Q2#
print("temperature_2m_max:", model.named_steps["logreg"].coef_[0][0])
print("temperature_2m_min:", model.named_steps["logreg"].coef_[0][1])
print("precipitation_sum", model.named_steps["logreg"].coef_[0][2])
print("wind_speed_10m_max", model.named_steps["logreg"].coef_[0][3])
# The wind_speed_10m_max feature pushes the model the strongest to "skip" a run. This didn't match what I had originially thought. I thought rain or low temp would do it.#
#Q3#
probalitities = model.predict_proba(X_test)[:,1]
print(probalitities[:5].round(2))
# A probablity of ).5 is saying that it is barely leaning towards good or skip for that day.#
                        #Evaluation#
#Q1#
labels = [0,1]
cm = confusion_matrix(y_test,y_pred1,labels=labels)
disp = ConfusionMatrixDisplay(confusion_matrix=cm,display_labels=["skip","good"])
disp.plot(colorbar=False)
plt.title("logreg_confusion_matrix")
plt.savefig('outputs/logreg_confusion_matrix.png')
plt.show()
# There were 7 False Negatives(meaning the model incorrectly predicted it was a bad day to run when it wasn't) and 9 False Positives (meaning the model incorrectly predicted it was a good day to run when it wasn't)#
                            #joblib#
#Q1#
#Saving/dumping it#
joblib.dump(model,"models/warmup_model.pkl")
print("Model saved.")
#Loading it#
loaded = joblib.load("models/warmup_model.pkl")
assert (loaded.predict(X_test) == model.predict(X_test)).all()
print("Predictions match.")
#If we have the model use raw data it could use numbers it hadn't learned from so the predictions could be wrong as a result of that.#