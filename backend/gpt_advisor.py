import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def get_advice(
    disease,
    risk
):

    prompt = f"""
    Disease: {disease}

    Risk Percentage: {risk}%

    Give:

    1. Disease explanation
    2. Diet recommendations
    3. Exercise recommendations
    4. Prevention tips
    5. Lifestyle changes

    Format neatly.
    """

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        return (
            response.choices[0]
            .message.content
        )

    except Exception as e:

        print(
            "Groq Error:",
            e
        )

        return (
            "Unable to generate advice currently."
        )


def estimate_missing_risk(
    disease,
    patient_data
):

    prompt = f"""
    You are a medical risk estimation AI.

    Disease:
    {disease}

    Patient Data:
    {patient_data}

    Estimate the probability
    of this disease.

    Consider:

    - Age
    - Gender
    - Hypertension
    - Heart disease
    - Stroke history
    - Chronic kidney disease
    - Cholesterol
    - Blood pressure
    - Glucose
    - BMI
    - Creatinine
    - Bilirubin
    - Albumin
    - Smoking history

    Return ONLY a number.

    Example:

    68
    """

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        value = (
            response.choices[0]
            .message.content
            .strip()
            .replace("%", "")
        )

        return float(value)

    except Exception as e:

        print(
            "Risk Estimation Error:",
            e
        )

        return 50.0


def generate_disease_recommendation(
    disease,
    risk,
    source="ML"
):

    prompt = f"""
    Disease:
    {disease}

    Risk:
    {risk}%

    Prediction Source:
    {source}

    Generate:

    1. Disease Overview
    2. Risk Interpretation
    3. Recommended Foods
    4. Foods To Avoid
    5. Exercise Plan
    6. Lifestyle Improvements
    7. Prevention Strategy

    Format professionally.
    """

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        return (
            response.choices[0]
            .message.content
        )

    except Exception as e:

        print(
            "Recommendation Error:",
            e
        )

        return (
            f"{disease} Risk: "
            f"{risk}% "
            f"(Source: {source})"
        )


def generate_final_health_report(
    patient_profile,
    disease_results
):

    prompt = f"""
    You are an expert physician.

    Patient Profile:

    {patient_profile}

    Disease Results:

    {disease_results}

    Generate a professional report.

    Include:

    1. Executive Summary
    2. Overall Health Status
    3. High Risk Diseases
    4. Medium Risk Diseases
    5. Low Risk Diseases
    6. Risk Explanations
    7. Diet Recommendations
    8. Exercise Recommendations
    9. Lifestyle Modifications
    10. Preventive Measures
    11. Suggested Medical Tests
    12. When To Consult A Doctor

    Format with proper headings.
    """

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        return (
            response.choices[0]
            .message.content
        )

    except Exception as e:

        print(
            "Health Report Error:",
            e
        )

        return (
            "AI health report could "
            "not be generated currently."
        )