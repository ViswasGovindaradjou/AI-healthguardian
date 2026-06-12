import json
import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def extract_medical_data(report_text):

    print("\n========== PDF TEXT ==========\n")
    print(report_text[:5000])

    prompt = f"""
    You are a medical data extraction system.

    Extract ONLY values useful for disease prediction.

    Return ONLY valid JSON.

    Do NOT return explanations.
    Do NOT return markdown.

    Extract if available:

    {{
        "age": number,
        "gender": "male/female",

        "glucose": number,
        "blood_pressure": number,
        "cholesterol": number,
        "bmi": number,
        "insulin": number,

        "creatinine": number,
        "blood_urea": number,
        "sodium": number,
        "potassium": number,

        "bilirubin": number,
        "albumin": number,
        "alkaline_phosphatase": number,
        "sgpt": number,
        "sgot": number,

        "hypertension": true,
        "heart_disease": true,
        "stroke_history": true,
        "smoking": true,

        "hemoglobin": number,
        "wbc": number,
        "platelets": number
    }}

    Omit fields that are not present.

    Medical Report:

    {report_text}
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

        text = (
            response.choices[0]
            .message.content
            .strip()
        )

        print(
            "\n========== GROQ RESPONSE ==========\n"
        )
        print(text)

        if text.startswith("```json"):
            text = (
                text.replace(
                    "```json",
                    ""
                )
                .replace(
                    "```",
                    ""
                )
                .strip()
            )

        elif text.startswith("```"):
            text = (
                text.replace(
                    "```",
                    ""
                )
                .strip()
            )

        data = json.loads(text)

        print(
            "\n========== EXTRACTED DATA ==========\n"
        )
        print(data)

        return data

    except Exception as e:

        print(
            "\n========== PARSER ERROR ==========\n"
        )

        print(e)

        return {}