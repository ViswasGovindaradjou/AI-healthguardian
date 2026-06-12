import joblib
import pandas as pd

# ==========================
# LOAD MODELS
# ==========================

diabetes_model = joblib.load(
    "models/diabetes_model.pkl"
)

heart_model = joblib.load(
    "models/heart_model.pkl"
)

kidney_model = joblib.load(
    "models/kidney_model.pkl"
)

liver_model = joblib.load(
    "models/liver_model.pkl"
)

stroke_model = joblib.load(
    "models/stroke_model.pkl"
)

# ==========================
# DIABETES
# Features:
# age, glucose, bmi, blood_pressure
# ==========================

def predict_diabetes(data):

    df = pd.DataFrame([{
        "age": data["Age"],
        "glucose": data["Glucose"],
        "bmi": data["BMI"],
        "blood_pressure": data["BloodPressure"]
    }])

    pred = diabetes_model.predict(df)[0]

    risk = (
        diabetes_model.predict_proba(df)[0][1]
        * 100
    )

    return int(pred), round(risk, 2)


# ==========================
# HEART
# Features:
# age, cholesterol,
# blood_pressure, bmi, smoking
# ==========================

def predict_heart(data):

    df = pd.DataFrame([{
        "age": data["age"],
        "cholesterol": data["chol"],
        "blood_pressure": data["trestbps"],
        "bmi": 30,
        "smoking": 0
    }])

    pred = heart_model.predict(df)[0]

    risk = (
        heart_model.predict_proba(df)[0][1]
        * 100
    )

    return int(pred), round(risk, 2)


# ==========================
# KIDNEY
# Features:
# age, creatinine,
# blood_urea, sodium,
# potassium
# ==========================

def predict_kidney(data):

    df = pd.DataFrame([{
        "age": data["age"],
        "creatinine": data["sc"],
        "blood_urea": data["bu"],
        "sodium": data["sod"],
        "potassium": data["pot"]
    }])

    pred = kidney_model.predict(df)[0]

    risk = (
        kidney_model.predict_proba(df)[0][1]
        * 100
    )

    return int(pred), round(risk, 2)


# ==========================
# LIVER
# Features:
# age, bilirubin,
# albumin, sgpt, sgot
# ==========================

def predict_liver(data):

    df = pd.DataFrame([{
        "age": data["Age"],
        "bilirubin": data["Total_Bilirubin"],
        "albumin": data["Albumin"],
        "sgpt": data["Alamine_Aminotransferase"],
        "sgot": data["Aspartate_Aminotransferase"]
    }])

    pred = liver_model.predict(df)[0]

    risk = (
        liver_model.predict_proba(df)[0][1]
        * 100
    )

    return int(pred), round(risk, 2)


# ==========================
# STROKE
# Features:
# age, glucose,
# bmi, blood_pressure,
# smoking
# ==========================

def predict_stroke(data):

    smoking = 1

    if str(
        data.get(
            "smoking_status",
            "never smoked"
        )
    ).lower() == "never smoked":

        smoking = 0

    df = pd.DataFrame([{
        "age": data["age"],
        "glucose": data["avg_glucose_level"],
        "bmi": data["bmi"],
        "blood_pressure": 140,
        "smoking": smoking
    }])

    pred = stroke_model.predict(df)[0]

    risk = (
        stroke_model.predict_proba(df)[0][1]
        * 100
    )

    return int(pred), round(risk, 2)