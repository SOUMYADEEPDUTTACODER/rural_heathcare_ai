import requests
from schemas import SymptomCheckRequest, SymptomCheckResponse
from config import GROQ_API_KEY, GROQ_MODEL, GROQ_BASE_URL


async def analyze_symptoms(request: SymptomCheckRequest, db) -> SymptomCheckResponse:
    if not GROQ_API_KEY:
        raise ValueError("Missing GROQ_API_KEY in environment.")

    text = request.text

    # -------------------------
    # Fetch patient profile if exists
    # -------------------------
    profile = await db["patients"].find_one({"patient_id": request.conversation_id})
    profile_context = ""
    if profile:
        allergies = ", ".join(profile.get("allergies", []))
        chronic = ", ".join(profile.get("chronic_conditions", []))
        meds = ", ".join(profile.get("medications", []))
        profile_context = f"\n\nPatient Profile:\n- Age: {profile.get('age')}\n- Sex: {profile.get('sex')}\n- Allergies: {allergies}\n- Chronic Conditions: {chronic}\n- Current Medications: {meds}"

    # -------------------------
    # Build prompt
    # -------------------------
    prompt = f"""
Patient symptoms: {text}
{profile_context}

Task: As a medical assistant, provide:
1. A short summary of the symptoms
2. Possible conditions (not a definitive diagnosis, just probabilities)
3. General lifestyle/precaution recommendations
4. Recommended medical tests (lab tests, imaging, etc.)
5. Suggested over-the-counter medicines or home remedies (safe, non-prescription only)

⚠️ Do not prescribe antibiotics or strong medications. Always advise consulting a doctor.
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.6
    }

    resp = requests.post(GROQ_BASE_URL, headers=headers, json=data)
    if resp.status_code != 200:
        raise RuntimeError(f"Groq API error: {resp.text}")

    ai_content = resp.json()["choices"][0]["message"]["content"]

    return SymptomCheckResponse(
        conversation_id=request.conversation_id,
        input_text=text,
        summary=f"Patient reports: {text}",
        probable_conditions=[ai_content],  # store raw AI output
        recommendations=["Consult doctor", "Follow safe medical practices"],
        recommended_tests=["Blood test", "Chest X-ray"],   # fallback examples
        recommended_medicines=["Paracetamol", "ORS"]       # fallback examples
    )
