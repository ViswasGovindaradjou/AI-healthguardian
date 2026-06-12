from pydantic import BaseModel


class DiabetesRequest(BaseModel):
    Pregnancies: float
    Glucose: float
    BloodPressure: float
    SkinThickness: float
    Insulin: float
    BMI: float
    DiabetesPedigreeFunction: float
    Age: float


class HeartRequest(BaseModel):
    age: float
    sex: float
    cp: float
    trestbps: float
    chol: float
    fbs: float
    restecg: float
    thalach: float
    exang: float
    oldpeak: float
    slope: float
    ca: float
    thal: float


class LiverRequest(BaseModel):
    Age: float
    Gender: float
    Total_Bilirubin: float
    Direct_Bilirubin: float
    Alkaline_Phosphotase: float
    Alamine_Aminotransferase: float
    Aspartate_Aminotransferase: float
    Total_Protiens: float
    Albumin: float
    Albumin_and_Globulin_Ratio: float


class AdviceRequest(BaseModel):
    disease: str
    risk: float


class KidneyRequest(BaseModel):
    age: float
    bp: float
    sg: float
    al: float
    su: float
    rbc: float
    pc: float
    pcc: float
    ba: float
    bgr: float
    bu: float
    sc: float
    sod: float
    pot: float
    hemo: float
    pcv: float
    wc: float
    rc: float
    htn: float
    dm: float
    cad: float
    appet: float
    pe: float
    ane: float


class StrokeRequest(BaseModel):
    gender: str
    age: float
    hypertension: int
    heart_disease: int
    ever_married: str
    work_type: str
    Residence_type: str
    avg_glucose_level: float
    bmi: float
    smoking_status: str