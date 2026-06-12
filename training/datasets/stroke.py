import pandas as pd
import numpy as np

np.random.seed(42)

rows = 10000

data = []

for _ in range(rows):

    age = np.random.randint(
        20,
        90
    )

    glucose = np.random.randint(
        70,
        350
    )

    bmi = round(
        np.random.uniform(
            18,
            45
        ),
        1
    )

    blood_pressure = np.random.randint(
        80,
        200
    )

    smoking = np.random.randint(
        0,
        2
    )

    stroke = 1 if (
        age > 60 and
        blood_pressure > 150 and
        glucose > 140
    ) else 0

    data.append([
        age,
        glucose,
        bmi,
        blood_pressure,
        smoking,
        stroke
    ])

df = pd.DataFrame(data, columns=[
    "age",
    "glucose",
    "bmi",
    "blood_pressure",
    "smoking",
    "stroke"
])

df.to_csv(
    "stroke.csv",
    index=False
)

print("Saved stroke_dataset.csv")