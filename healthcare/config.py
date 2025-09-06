# config.py
import os
from dotenv import load_dotenv

# Load variables from .env file into environment
load_dotenv()

# Whisper model (local) - choose "tiny" or "base" depending on CPU capacity
WHISPER_MODEL_NAME = os.getenv("WHISPER_MODEL", "base")

# MongoDB connection (local by default, can be swapped with Atlas URI)
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "rural_healthcare")

# Groq API
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
GROQ_BASE_URL = "https://api.groq.com/openai/v1/chat/completions"
