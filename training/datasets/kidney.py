import pandas as pd
import numpy as np

np.random.seed(42)

rows = 10000

data = []

for _ in range(rows):

    age = np.random.randint(20, 90)

    creatinine = round(
        np.random.uniform(0.5, 5.0),
        2
    )

    blood_urea = np.random.randint(
        10,
        120
    )

    sodium = np.random.randint(
        120,
        155
    )

    potassium = round(
        np.random.uniform(
            2.5,
            7.0
        ),
        1
    )

    kidney = 1 if (
        creatinine > 1.5 or
        blood_urea > 50
    ) else 0

    data.append([
        age,
        creatinine,
        blood_urea,
        sodium,
        potassium,
        kidney
    ])

df = pd.DataFrame(data, columns=[
    "age",
    "creatinine",
    "blood_urea",
    "sodium",
    "potassium",
    "kidney"
])

df.to_csv(
    "kidney_dataset.csv",
    index=False
)

print("Saved kidney.csv")