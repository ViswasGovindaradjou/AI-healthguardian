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

    bilirubin = round(
        np.random.uniform(
            0.1,
            8
        ),
        2
    )

    albumin = round(
        np.random.uniform(
            2,
            5.5
        ),
        1
    )

    sgpt = np.random.randint(
        10,
        250
    )

    sgot = np.random.randint(
        10,
        250
    )

    liver = 1 if (
        bilirubin > 1.2 or
        sgpt > 60 or
        sgot > 60
    ) else 0

    data.append([
        age,
        bilirubin,
        albumin,
        sgpt,
        sgot,
        liver
    ])

df = pd.DataFrame(data, columns=[
    "age",
    "bilirubin",
    "albumin",
    "sgpt",
    "sgot",
    "liver"
])

df.to_csv(
    "liver_dataset.csv",
    index=False
)

print("Saved liver.csv")