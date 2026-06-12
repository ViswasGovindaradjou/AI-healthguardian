import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("datasets/heart.csv")

X = df[
    [
        "age",
        "cholesterol",
        "blood_pressure",
        "bmi",
        "smoking"
    ]
]

y = df["heart"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

joblib.dump(
    model,
    "models/heart_model.pkl"
)

print("Heart Model Saved")