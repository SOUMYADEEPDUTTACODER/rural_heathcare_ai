import requests
from deep_translator import GoogleTranslator
from config import GROQ_API_KEY, GROQ_MODEL, GROQ_BASE_URL
from schemas import ChatRequest, ChatResponse, ChatMessage


async def doctor_patient_chat(request: ChatRequest, db) -> ChatResponse:
    if not GROQ_API_KEY:
        raise ValueError("Missing GROQ_API_KEY in environment.")

    # Step 1: Translate patient message -> English
    patient_msg_en = GoogleTranslator(source="auto", target=request.target_lang).translate(request.message)

    # -------------------------
    # Fetch patient profile
    # -------------------------
    profile = await db["patients"].find_one({"patient_id": request.conversation_id})
    profile_context = ""
    if profile:
        allergies = ", ".join(profile.get("allergies", []))
        chronic = ", ".join(profile.get("chronic_conditions", []))
        meds = ", ".join(profile.get("medications", []))
        profile_context = f"\n\nPatient Profile:\n- Age: {profile.get('age')}\n- Sex: {profile.get('sex')}\n- Allergies: {allergies}\n- Chronic Conditions: {chronic}\n- Current Medications: {meds}"

    # Step 2: Send to Groq AI
    prompt = f"""
Patient message (in English): {patient_msg_en}
{profile_context}

Task: You are a doctor in a rural telemedicine setting.
Respond clearly and simply, avoiding medical jargon.
Always include follow-up questions if needed.
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

    doctor_msg_en = resp.json()["choices"][0]["message"]["content"]

    # Step 3: Translate doctor response back to patient language
    doctor_msg_patient_lang = GoogleTranslator(source="auto", target=request.source_lang).translate(doctor_msg_en)

    # Step 4: Prepare chat messages
    patient_entry = ChatMessage(role="patient", text=request.message, translated_text=patient_msg_en)
    doctor_entry = ChatMessage(role="doctor", text=doctor_msg_patient_lang, translated_text=doctor_msg_en)

    # Step 5: Save to DB
    conversation = await db["chats"].find_one({"conversation_id": request.conversation_id})
    if not conversation:
        conversation = {"conversation_id": request.conversation_id, "history": []}

    conversation["history"].append(patient_entry.dict())
    conversation["history"].append(doctor_entry.dict())

    await db["chats"].update_one(
        {"conversation_id": request.conversation_id},
        {"$set": {"history": conversation["history"]}},
        upsert=True
    )

    return ChatResponse(conversation_id=request.conversation_id, history=conversation["history"])
