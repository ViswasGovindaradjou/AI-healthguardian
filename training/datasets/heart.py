import pandas as pd
import numpy as np

np.random.seed(42)

rows = 10000

data = []

for _ in range(rows):

    age = np.random.randint(20, 90)
    cholesterol = np.random.randint(120, 400)
    bp = np.random.randint(80, 200)
    bmi = round(np.random.uniform(18, 45), 1)
    smoking = np.random.randint(0, 2)

    heart = 1 if (
        age > 55 and
        cholesterol > 220 and
        bp > 140
    ) else 0

    data.append([
        age,
        cholesterol,
        bp,
        bmi,
        smoking,
        heart
    ])

df = pd.DataFrame(data, columns=[
    "age",
    "cholesterol",
    "blood_pressure",
    "bmi",
    "smoking",
    "heart"
])

df.to_csv("heart.csv", index=False)
print("Saved heart_dataset.csv")