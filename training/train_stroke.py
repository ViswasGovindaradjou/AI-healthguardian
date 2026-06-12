import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("datasets/stroke.csv")

X = df[
    [
        "age",
        "glucose",
        "bmi",
        "blood_pressure",
        "smoking"
    ]
]

y = df["stroke"]

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
    "models/stroke_model.pkl"
)

print("Stroke Model Saved")