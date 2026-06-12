import pandas as pd
import joblib

df = pd.read_csv("datasets/stroke.csv")

df.drop("id", axis=1, inplace=True)

df["bmi"] = df["bmi"].fillna(
    df["bmi"].median()
)

X = df.drop("stroke", axis=1)

X = pd.get_dummies(
    X,
    drop_first=True
)

joblib.dump(
    list(X.columns),
    "models/stroke_columns.pkl"
)

print("Stroke columns saved")