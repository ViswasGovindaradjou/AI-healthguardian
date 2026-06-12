from backend.predictor import (
    predict_diabetes,
    predict_heart,
    predict_kidney,
    predict_liver,
    predict_stroke
)

from backend.gpt_advisor import (
    generate_final_health_report
)

REQUIREMENTS = {

    "diabetes": [
        "glucose",
        "bmi",
        "age"
    ],

    "heart": [
        "age",
        "blood_pressure",
        "cholesterol"
    ],

    "kidney": [
        "creatinine"
    ],

    "liver": [
        "bilirubin",
        "albumin"
    ],

    "stroke": [
        "age",
        "glucose"
    ]
}


def has_required_fields(profile, fields):

    return all(
        profile.get(field) is not None
        for field in fields
    )


def estimate_missing_risk(
    disease_name,
    patient_profile,
    existing_ml_results
):
    """
    AI reasoning-based risk estimation for missing disease predictions.
    
    Analyzes:
    - Patient profile and available biomarkers
    - Existing ML predictions
    - Disease relationships and risk propagation
    
    Returns: Medically reasonable risk percentage (0-95)
    """

    risk = 0
    age = patient_profile.get("age", 40)
    glucose = patient_profile.get("glucose", 100)
    bp = patient_profile.get("blood_pressure", 120)
    bmi = patient_profile.get("bmi", 25)
    hypertension = patient_profile.get("hypertension", False)

    # =============================================
    # DIABETES RISK ESTIMATION
    # =============================================

    if disease_name == "diabetes":

        # Direct biomarker analysis
        if glucose >= 200:
            risk += 30
        elif glucose >= 140:
            risk += 20
        elif glucose >= 126:
            risk += 15

        if age >= 55:
            risk += 15
        elif age >= 45:
            risk += 8

        if bmi >= 30:
            risk += 15
        elif bmi >= 25:
            risk += 8

        if hypertension:
            risk += 10

        if patient_profile.get("heart_disease", False):
            risk += 8

        # Risk propagation from existing predictions
        if "heart" in existing_ml_results and existing_ml_results["heart"]["risk"]:
            heart_risk = existing_ml_results["heart"]["risk"]
            if heart_risk > 70:
                risk += 12
            elif heart_risk > 50:
                risk += 6

        return min(risk, 95)

    # =============================================
    # HEART RISK ESTIMATION
    # =============================================

    elif disease_name == "heart":

        # Direct biomarker analysis
        if age >= 60:
            risk += 20
        elif age >= 50:
            risk += 12
        elif age >= 40:
            risk += 6

        if bp >= 160:
            risk += 25
        elif bp >= 140:
            risk += 18
        elif bp >= 130:
            risk += 10

        cholesterol = patient_profile.get("cholesterol", 180)
        if cholesterol >= 240:
            risk += 15
        elif cholesterol >= 200:
            risk += 10

        if hypertension:
            risk += 12

        if patient_profile.get("heart_disease", False):
            risk += 20

        # Risk propagation from existing predictions
        if "diabetes" in existing_ml_results and existing_ml_results["diabetes"]["risk"]:
            diabetes_risk = existing_ml_results["diabetes"]["risk"]
            if diabetes_risk > 70:
                risk += 15
            elif diabetes_risk > 50:
                risk += 10

        if "stroke" in existing_ml_results and existing_ml_results["stroke"]["risk"]:
            stroke_risk = existing_ml_results["stroke"]["risk"]
            if stroke_risk > 60:
                risk += 10

        return min(risk, 95)

    # =============================================
    # KIDNEY RISK ESTIMATION
    # =============================================

    elif disease_name == "kidney":

        # Glucose impact on kidney (strong indicator)
        if glucose >= 200:
            risk += 20
        elif glucose >= 140:
            risk += 12

        # Blood pressure impact
        if bp >= 160:
            risk += 25
        elif bp >= 140:
            risk += 18
        elif bp >= 130:
            risk += 10

        # Age factor
        if age >= 60:
            risk += 12
        elif age >= 50:
            risk += 6

        if hypertension:
            risk += 15

        # Risk propagation from diabetes (strong relationship)
        if "diabetes" in existing_ml_results and existing_ml_results["diabetes"]["risk"]:
            diabetes_risk = existing_ml_results["diabetes"]["risk"]
            if diabetes_risk > 75:
                risk += 20
            elif diabetes_risk > 60:
                risk += 15
            elif diabetes_risk > 40:
                risk += 8

        # Risk propagation from heart disease
        if "heart" in existing_ml_results and existing_ml_results["heart"]["risk"]:
            heart_risk = existing_ml_results["heart"]["risk"]
            if heart_risk > 70:
                risk += 12

        # Combined risk factors
        if hypertension and glucose >= 140:
            risk += 10

        return min(risk, 95)

    # =============================================
    # LIVER RISK ESTIMATION
    # =============================================

    elif disease_name == "liver":

        # Direct biomarker analysis if available
        bilirubin = patient_profile.get("bilirubin", 0.7)
        albumin = patient_profile.get("albumin", 3.5)

        if bilirubin >= 1.2:
            risk += 30
        elif bilirubin >= 0.8:
            risk += 15

        if albumin < 3.0:
            risk += 25
        elif albumin < 3.5:
            risk += 18
        elif albumin < 4.0:
            risk += 10

        # Age consideration
        if age >= 55:
            risk += 8

        # Risk propagation from diabetes
        if "diabetes" in existing_ml_results and existing_ml_results["diabetes"]["risk"]:
            diabetes_risk = existing_ml_results["diabetes"]["risk"]
            if diabetes_risk > 75:
                risk += 12
            elif diabetes_risk > 50:
                risk += 6

        # Risk propagation from heart
        if "heart" in existing_ml_results and existing_ml_results["heart"]["risk"]:
            heart_risk = existing_ml_results["heart"]["risk"]
            if heart_risk > 70:
                risk += 8

        # Obesity impact
        if bmi >= 30:
            risk += 10
        elif bmi >= 25:
            risk += 5

        # Combined metabolic syndrome indicator
        if glucose >= 140 and hypertension and bmi >= 25:
            risk += 10

        return min(risk, 95)

    # =============================================
    # STROKE RISK ESTIMATION
    # =============================================

    elif disease_name == "stroke":

        # Direct biomarker analysis
        if age >= 70:
            risk += 20
        elif age >= 60:
            risk += 15
        elif age >= 50:
            risk += 8

        if bp >= 160:
            risk += 25
        elif bp >= 140:
            risk += 18
        elif bp >= 130:
            risk += 10

        if glucose >= 200:
            risk += 20
        elif glucose >= 140:
            risk += 12

        if hypertension:
            risk += 15

        if patient_profile.get("stroke_history", False):
            risk += 20

        if patient_profile.get("heart_disease", False):
            risk += 15

        # Risk propagation from heart disease
        if "heart" in existing_ml_results and existing_ml_results["heart"]["risk"]:
            heart_risk = existing_ml_results["heart"]["risk"]
            if heart_risk > 75:
                risk += 15
            elif heart_risk > 60:
                risk += 10

        # Risk propagation from diabetes
        if "diabetes" in existing_ml_results and existing_ml_results["diabetes"]["risk"]:
            diabetes_risk = existing_ml_results["diabetes"]["risk"]
            if diabetes_risk > 70:
                risk += 10
            elif diabetes_risk > 50:
                risk += 6

        # Risk propagation from kidney disease
        if "kidney" in existing_ml_results and existing_ml_results["kidney"]["risk"]:
            kidney_risk = existing_ml_results["kidney"]["risk"]
            if kidney_risk > 70:
                risk += 8

        # Smoking status impact
        if patient_profile.get("smoking", False):
            risk += 12

        return min(risk, 95)

    # Default fallback
    return 0


def analyze_patient(patient_profile):

    results = {}

    age = patient_profile.get("age", 40)

    gender = str(
        patient_profile.get(
            "gender",
            "male"
        )
    ).lower()

    # ======================
    # DIABETES
    # ======================

    if has_required_fields(
        patient_profile,
        REQUIREMENTS["diabetes"]
    ):

        try:

            _, risk = predict_diabetes({

                "Pregnancies": 0,
                "Glucose": patient_profile["glucose"],

                "BloodPressure":
                patient_profile.get(
                    "blood_pressure",
                    80
                ),

                "SkinThickness": 20,

                "Insulin":
                patient_profile.get(
                    "insulin",
                    85
                ),

                "BMI":
                patient_profile["bmi"],

                "DiabetesPedigreeFunction":
                0.5,

                "Age": age
            })

            source = "ML"

        except Exception as e:

            print("Diabetes ML Error:", e)

            risk = estimate_missing_risk(
                "diabetes",
                patient_profile,
                results
            )

            source = "AI Reasoning"

    else:

        risk = estimate_missing_risk(
            "diabetes",
            patient_profile,
            results
        )

        source = "AI Reasoning"

    results["diabetes"] = {
        "risk": risk,
        "source": source
    }

    # ======================
    # HEART
    # ======================

    if has_required_fields(
        patient_profile,
        REQUIREMENTS["heart"]
    ):

        try:

            _, risk = predict_heart({

                "age": age,

                "cholesterol":
                patient_profile[
                    "cholesterol"
                ],

                "blood_pressure":
                patient_profile[
                    "blood_pressure"
                ],

                "bmi":
                patient_profile.get(
                    "bmi",
                    25
                ),

                "smoking":
                1 if patient_profile.get(
                    "smoking",
                    False
                ) else 0

            })

            source = "ML"

        except Exception as e:

            print("Heart ML Error:", e)

            risk = estimate_missing_risk(
                "heart",
                patient_profile,
                results
            )

            source = "AI Reasoning"

    else:

        risk = estimate_missing_risk(
            "heart",
            patient_profile,
            results
        )

        source = "AI Reasoning"

    results["heart"] = {
        "risk": risk,
        "source": source
    }

    # ======================
    # KIDNEY
    # ======================

    if has_required_fields(
        patient_profile,
        REQUIREMENTS["kidney"]
    ):

        try:

            _, risk = predict_kidney({

                "age": age,

                "bp":
                patient_profile.get(
                    "blood_pressure",
                    80
                ),

                "sg": 1.02,
                "al": 0,
                "su": 0,
                "rbc": 1,
                "pc": 1,
                "pcc": 0,
                "ba": 0,

                "bgr":
                patient_profile.get(
                    "glucose",
                    120
                ),

                "bu":
                patient_profile.get(
                    "blood_urea",
                    20
                ),

                "sc":
                patient_profile[
                    "creatinine"
                ],

                "sod":
                patient_profile.get(
                    "sodium",
                    135
                ),

                "pot":
                patient_profile.get(
                    "potassium",
                    4.5
                ),

                "hemo":
                patient_profile.get(
                    "hemoglobin",
                    14
                ),

                "pcv": 45,

                "wc":
                patient_profile.get(
                    "wbc",
                    8000
                ),

                "rc": 5,

                "htn":
                1 if patient_profile.get(
                    "hypertension",
                    False
                ) else 0,

                "dm": 0,
                "cad": 0,
                "appet": 1,
                "pe": 0,
                "ane": 0
            })

            source = "ML"

        except Exception as e:

            print("Kidney ML Error:", e)

            risk = estimate_missing_risk(
                "kidney",
                patient_profile,
                results
            )

            source = "AI Reasoning"

    else:

        risk = estimate_missing_risk(
            "kidney",
            patient_profile,
            results
        )

        source = "AI Reasoning"

    results["kidney"] = {
        "risk": risk,
        "source": source
    }

    # ======================
    # LIVER
    # ======================

    if has_required_fields(
        patient_profile,
        REQUIREMENTS["liver"]
    ):

        try:

            _, risk = predict_liver({

                "Age": age,

                "Gender":
                1 if gender == "male"
                else 0,

                "Total_Bilirubin":
                patient_profile[
                    "bilirubin"
                ],

                "Direct_Bilirubin": 0.3,

                "Alkaline_Phosphotase":
                patient_profile.get(
                    "alkaline_phosphatase",
                    200
                ),

                "Alamine_Aminotransferase":
                patient_profile.get(
                    "sgpt",
                    30
                ),

                "Aspartate_Aminotransferase":
                patient_profile.get(
                    "sgot",
                    30
                ),

                "Total_Protiens": 7,

                "Albumin":
                patient_profile[
                    "albumin"
                ],

                "Albumin_and_Globulin_Ratio":
                1.2
            })

            source = "ML"

        except Exception as e:

            print("Liver ML Error:", e)

            risk = estimate_missing_risk(
                "liver",
                patient_profile,
                results
            )

            source = "AI Reasoning"

    else:

        risk = estimate_missing_risk(
            "liver",
            patient_profile,
            results
        )

        source = "AI Reasoning"

    results["liver"] = {
        "risk": risk,
        "source": source
    }

    # ======================
    # STROKE
    # ======================

    if has_required_fields(
        patient_profile,
        REQUIREMENTS["stroke"]
    ):

        try:

            _, risk = predict_stroke({

                "gender":
                "Male" if gender == "male"
                else "Female",

                "age": age,

                "hypertension":
                1 if patient_profile.get(
                    "hypertension",
                    False
                ) else 0,

                "heart_disease":
                1 if patient_profile.get(
                    "heart_disease",
                    False
                ) else 0,

                "ever_married": "Yes",
                "work_type": "Private",
                "Residence_type": "Urban",

                "avg_glucose_level":
                patient_profile[
                    "glucose"
                ],

                "bmi":
                patient_profile.get(
                    "bmi",
                    25
                ),

                "smoking_status":
                "formerly smoked"
                if patient_profile.get(
                    "smoking",
                    False
                )
                else "never smoked"
            })

            source = "ML"

            # Stroke risk correction
            if risk < 5:
                glucose = patient_profile.get("glucose", 100)
                bp = patient_profile.get("blood_pressure", 120)

                if glucose > 180 or bp > 140:
                    risk = 40
                    source = "AI Corrected"

        except Exception as e:

            print("Stroke ML Error:", e)

            risk = estimate_missing_risk(
                "stroke",
                patient_profile,
                results
            )

            source = "AI Reasoning"

    else:

        risk = estimate_missing_risk(
            "stroke",
            patient_profile,
            results
        )

        source = "AI Reasoning"

    results["stroke"] = {
        "risk": risk,
        "source": source
    }

    valid_results = {}

    for disease, data in results.items():

        if data["risk"] is not None:
            valid_results[disease] = data

    try:

        final_report = (
            generate_final_health_report(
                patient_profile,
                valid_results
            )
        )

    except Exception as e:

        print("Report Error:", e)

        final_report = (
            "Health report generation failed."
        )

    return {

        "patient_profile":
        patient_profile,

        "results":
        results,

        "final_report":
        final_report
    }