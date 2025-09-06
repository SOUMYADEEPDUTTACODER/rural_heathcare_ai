from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

# ---------- STT + Translation ----------
class STTResponse(BaseModel):
    original_text: str
    translated_text: str
    target_lang: str


# ---------- Message / Chat ----------
class MessageCreate(BaseModel):
    conversation_id: str
    sender_role: str  # "patient" or "doctor"
    text: str
    translated_text: Optional[str] = None
    language: Optional[str] = "auto"


class MessageResponse(MessageCreate):
    id: str = Field(..., alias="_id")  # MongoDB ObjectId
    created_at: datetime


# Chat message schema
class ChatMessage(BaseModel):
    role: str  # "patient" or "doctor"
    text: str
    translated_text: Optional[str] = None


class ChatRequest(BaseModel):
    conversation_id: str
    message: str
    source_lang: str = "auto"  # patient input language
    target_lang: str = "en"    # language for AI processing


class ChatResponse(BaseModel):
    conversation_id: str
    history: List[ChatMessage]


# ---------- Transcript ----------
class TranscriptCreate(BaseModel):
    conversation_id: str
    original_filename: str
    transcript_text: str
    language: Optional[str] = "auto"


class TranscriptResponse(TranscriptCreate):
    id: str = Field(..., alias="_id")
    created_at: datetime


# ---------- Symptom Checker ----------
class SymptomCheckRequest(BaseModel):
    conversation_id: str
    text: str
    language: Optional[str] = "en"
    age: Optional[int] = None
    sex: Optional[str] = None


class SymptomCheckResponse(BaseModel):
    conversation_id: str
    input_text: str
    summary: str
    probable_conditions: List[str]
    recommendations: List[str]
    recommended_tests: List[str] = []
    recommended_medicines: List[str] = []


# ---------- Patient Profiles ----------
class PatientProfileCreate(BaseModel):
    patient_id: str
    name: str
    age: int
    sex: str
    allergies: Optional[List[str]] = []
    chronic_conditions: Optional[List[str]] = []
    medications: Optional[List[str]] = []


class PatientProfileResponse(PatientProfileCreate):
    id: str = Field(..., alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
