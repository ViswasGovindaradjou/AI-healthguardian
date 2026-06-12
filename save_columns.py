import pandas as pd
import joblib

# Diabetes
df = pd.read_csv("datasets/diabetes.csv")
joblib.dump(
    list(df.drop("Outcome", axis=1).columns),
    "models/diabetes_columns.pkl"
)

# Heart
df = pd.read_csv("datasets/heart.csv")
joblib.dump(
    list(df.drop("target", axis=1).columns),
    "models/heart_columns.pkl"
)

# Liver
df = pd.read_csv("datasets/liver.csv")
joblib.dump(
    list(df.drop("Dataset", axis=1).columns),
    "models/liver_columns.pkl"
)

print("Columns Saved")