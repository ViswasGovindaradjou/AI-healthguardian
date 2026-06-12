import pandas as pd
import joblib

df = pd.read_csv("datasets/kidney.csv")

df.drop("id", axis=1, inplace=True)

joblib.dump(
    list(df.drop("classification", axis=1).columns),
    "models/kidney_columns.pkl"
)

print("Kidney columns saved")