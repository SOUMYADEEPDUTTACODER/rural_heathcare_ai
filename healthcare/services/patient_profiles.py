from schemas import PatientProfileCreate, PatientProfileResponse
from datetime import datetime
from bson import ObjectId

async def create_patient_profile(profile: PatientProfileCreate, db) -> PatientProfileResponse:
    doc = profile.dict()
    doc["created_at"] = datetime.utcnow()
    result = await db["patients"].insert_one(doc)
    doc["_id"] = str(result.inserted_id)
    return PatientProfileResponse(**doc)

async def get_patient_profile(patient_id: str, db):
    profile = await db["patients"].find_one({"patient_id": patient_id})
    if profile:
        profile["_id"] = str(profile["_id"])
        return PatientProfileResponse(**profile)
    return None
