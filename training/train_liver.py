import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("datasets/liver.csv")

X = df[
    [
        "age",
        "bilirubin",
        "albumin",
        "sgpt",
        "sgot"
    ]
]

y = df["liver"]

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
    "models/liver_model.pkl"
)

print("Liver Model Saved")