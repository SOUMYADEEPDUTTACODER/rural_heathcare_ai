# services/stt_translate.py
import tempfile
import whisper
from deep_translator import GoogleTranslator
from config import WHISPER_MODEL_NAME

# Global Whisper model (loaded once at startup)
whisper_model = None

async def init_whisper():
    """
    Initialize Whisper model once during FastAPI startup.
    """
    global whisper_model
    if whisper_model is None:
        whisper_model = whisper.load_model(WHISPER_MODEL_NAME)
        print(f"✅ Whisper model '{WHISPER_MODEL_NAME}' loaded successfully.")

async def speech_to_text_and_translate(file, target_lang: str = "en"):
    """
    Transcribe speech to text and translate to target language.
    Supports .mp3, .wav, .webm, and .ogg files.
    """
    try:
        # Detect file extension
        filename = file.filename.lower()
        if filename.endswith(".mp3"):
            suffix = ".mp3"
        elif filename.endswith(".wav"):
            suffix = ".wav"
        elif filename.endswith(".webm"):
            suffix = ".webm"
        elif filename.endswith(".ogg"):
            suffix = ".ogg"
        else:
            suffix = ".wav"  # fallback to .wav

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await file.read())
            audio_path = tmp.name

        # Step 1: Transcribe with loaded Whisper model
        result = whisper_model.transcribe(audio_path)
        detected_text = result["text"]

        # Step 2: Translate
        translation = GoogleTranslator(source="auto", target=target_lang).translate(detected_text)

        return {
            "original_text": detected_text.strip(),
            "translated_text": translation.strip(),
            "target_lang": target_lang,
        }

    except Exception as e:
        return {"error": str(e)}
