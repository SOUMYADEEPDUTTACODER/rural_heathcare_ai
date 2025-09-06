# models.py
from datetime import datetime
from typing import Optional, List, Dict

# These are just helper dict "blueprints" for MongoDB inserts (not strict schemas)

def message_model(conversation_id: str, sender_role: str, text: str,
                  translated_text: Optional[str] = None, language: str = "auto") -> dict:
    return {
        "conversation_id": conversation_id,
        "sender_role": sender_role,   # "patient" or "doctor"
        "text": text,
        "translated_text": translated_text,
        "language": language,
        "created_at": datetime.utcnow()
    }

def transcript_model(conversation_id: str, original_filename: str,
                     transcript_text: str, language: str = "auto") -> dict:
    return {
        "conversation_id": conversation_id,
        "original_filename": original_filename,
        "transcript_text": transcript_text,
        "language": language,
        "created_at": datetime.utcnow()
    }
