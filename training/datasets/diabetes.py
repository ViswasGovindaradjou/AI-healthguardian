import pandas as pd
import numpy as np

np.random.seed(42)

rows = 10000

data = []

for _ in range(rows):

    age = np.random.randint(18, 85)
    glucose = np.random.randint(70, 350)
    bmi = round(np.random.uniform(18, 45), 1)
    bp = np.random.randint(80, 180)

    diabetes = 1 if (
        glucose > 140 or
        bmi > 30 or
        (age > 50 and glucose > 120)
    ) else 0

    data.append([
        age,
        glucose,
        bmi,
        bp,
        diabetes
    ])

df = pd.DataFrame(data, columns=[
    "age",
    "glucose",
    "bmi",
    "blood_pressure",
    "diabetes"
])

df.to_csv("diabetes.csv", index=False)
print("Saved diabetes.csv")