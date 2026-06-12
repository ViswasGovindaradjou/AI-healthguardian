from fastapi import (
    FastAPI,
    UploadFile,
    File
)

from fastapi.middleware.cors import CORSMiddleware

import fitz

from backend.schemas import (
    DiabetesRequest,
    HeartRequest,
    LiverRequest,
    KidneyRequest,
    StrokeRequest,
    AdviceRequest
)

from backend.predictor import (
    predict_diabetes,
    predict_heart,
    predict_liver,
    predict_kidney,
    predict_stroke
)

from backend.gpt_advisor import (
    get_advice
)

from backend.report_parser import (
    extract_medical_data
)

from backend.report_analyzer import (
    analyze_patient
)

app = FastAPI(
    title="AI Health Guardian"
)

# CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# PDF TEXT EXTRACTION
# -------------------------

def extract_pdf_text(pdf_bytes):

    text = ""

    try:

        pdf = fitz.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        print(
            f"PDF Pages: {len(pdf)}"
        )

        for page in pdf:

            page_text = (
                page.get_text()
            )

            text += page_text

        return text

    except Exception as e:

        print(
            "PDF Extraction Error:",
            e
        )

        return ""


# -------------------------
# HOME
# -------------------------

@app.get("/")
def home():

    return {
        "message":
        "AI Health Guardian Running"
    }


# -------------------------
# DIABETES
# -------------------------

@app.post("/predict/diabetes")
def diabetes(
    request: DiabetesRequest
):

    pred, risk = predict_diabetes(
        request.dict()
    )

    return {
        "prediction": int(pred),
        "risk_percentage": float(risk)
    }


# -------------------------
# HEART
# -------------------------

@app.post("/predict/heart")
def heart(
    request: HeartRequest
):

    pred, risk = predict_heart(
        request.dict()
    )

    return {
        "prediction": int(pred),
        "risk_percentage": float(risk)
    }


# -------------------------
# LIVER
# -------------------------

@app.post("/predict/liver")
def liver(
    request: LiverRequest
):

    pred, risk = predict_liver(
        request.dict()
    )

    return {
        "prediction": int(pred),
        "risk_percentage": float(risk)
    }


# -------------------------
# KIDNEY
# -------------------------

@app.post("/predict/kidney")
def kidney(
    request: KidneyRequest
):

    pred, risk = predict_kidney(
        request.dict()
    )

    return {
        "prediction": int(pred),
        "risk_percentage": float(risk)
    }


# -------------------------
# STROKE
# -------------------------

@app.post("/predict/stroke")
def stroke(
    request: StrokeRequest
):

    pred, risk = predict_stroke(
        request.dict()
    )

    return {
        "prediction": int(pred),
        "risk_percentage": float(risk)
    }


# -------------------------
# GEMINI ADVICE
# -------------------------

@app.post("/generate-advice")
def generate_advice(
    request: AdviceRequest
):

    advice = get_advice(
        request.disease,
        request.risk
    )

    return {
        "disease": request.disease,
        "risk": request.risk,
        "advice": advice
    }


# -------------------------
# REPORT ANALYZER
# -------------------------

@app.post("/analyze-report")
async def analyze_report(
    file: UploadFile = File(...)
):

    try:

        content = await file.read()

        filename = (
            file.filename.lower()
        )

        print("\n==============================")
        print("FILE RECEIVED:", filename)
        print("==============================\n")

        # PDF REPORT

        if filename.endswith(".pdf"):

            report_text = (
                extract_pdf_text(
                    content
                )
            )

        # IMAGE REPORT

        elif (
            filename.endswith(".jpg")
            or filename.endswith(".jpeg")
            or filename.endswith(".png")
        ):

            report_text = (
                "IMAGE_REPORT"
            )

        else:

            return {
                "error":
                "Supported formats: PDF, JPG, JPEG, PNG"
            }

        print(
            "\n========== REPORT TEXT ==========\n"
        )

        print(
            report_text[:5000]
        )

        patient_profile = (
            extract_medical_data(
                report_text
            )
        )

        print(
            "\n========== PATIENT PROFILE ==========\n"
        )

        print(
            patient_profile
        )

        analysis = (
            analyze_patient(
                patient_profile
            )
        )

        return analysis

    except Exception as e:

        print(
            "\n========== ANALYZE REPORT ERROR ==========\n"
        )

        print(str(e))

        return {
            "error": str(e)
        }