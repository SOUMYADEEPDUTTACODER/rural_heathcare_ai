# app.py
from fastapi import FastAPI, UploadFile, Depends
from services.stt_translate import speech_to_text_and_translate, init_whisper
from services.symptom_checker import analyze_symptoms
from services.chat import doctor_patient_chat
from services.patient_profiles import create_patient_profile, get_patient_profile
from schemas import (
    STTResponse,
    SymptomCheckRequest,
    SymptomCheckResponse,
    ChatRequest,
    ChatResponse,
    PatientProfileCreate,
    PatientProfileResponse,
)
from database import get_db
from config import WHISPER_MODEL_NAME

app = FastAPI(title="Rural Healthcare API (MongoDB)")

# -------------------------------
# Startup: load Whisper once
# -------------------------------
@app.on_event("startup")
async def startup_event():
    await init_whisper()
    print(f"✅ Whisper model '{WHISPER_MODEL_NAME}' initialized successfully.")


# -------------------------------
# Speech-to-text + Translation
# -------------------------------
@app.post("/stt-translate/", response_model=STTResponse)
async def stt_translate(file: UploadFile, target_lang: str = "en", db=Depends(get_db)):
    result = await speech_to_text_and_translate(file, target_lang)
    await db["transcripts"].insert_one(result)
    return result


# -------------------------------
# Symptom Checker (Groq API)
# -------------------------------
@app.post("/symptom-check/", response_model=SymptomCheckResponse)
async def symptom_check(request: SymptomCheckRequest, db=Depends(get_db)):
    result = await analyze_symptoms(request, db)
    await db["symptom_checks"].insert_one(result.dict())
    return result


# -------------------------------
# Doctor–Patient Chat (Groq + Translation)
# -------------------------------
@app.post("/chat/", response_model=ChatResponse)
async def chat(request: ChatRequest, db=Depends(get_db)):
    result = await doctor_patient_chat(request, db)
    return result


@app.get("/chat/{conversation_id}", response_model=ChatResponse)
async def get_chat_history(conversation_id: str, db=Depends(get_db)):
    """
    Retrieve full chat history by conversation_id.
    """
    conversation = await db["chats"].find_one({"conversation_id": conversation_id})
    if not conversation:
        return ChatResponse(conversation_id=conversation_id, history=[])
    return ChatResponse(conversation_id=conversation_id, history=conversation["history"])


# -------------------------------
# Patient Profiles
# -------------------------------
@app.post("/patients/", response_model=PatientProfileResponse)
async def add_patient(profile: PatientProfileCreate, db=Depends(get_db)):
    return await create_patient_profile(profile, db)


@app.get("/patients/{patient_id}", response_model=PatientProfileResponse)
async def fetch_patient(patient_id: str, db=Depends(get_db)):
    profile = await get_patient_profile(patient_id, db)
    if not profile:
        return {"error": "Patient not found"}
    return profile
