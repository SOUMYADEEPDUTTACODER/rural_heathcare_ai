# 🩺 Rural Healthcare AI Platform

A telemedicine platform for rural healthcare, combining **FastAPI backend** (AI + patient data) with a **Streamlit frontend** for easy use.  
It supports **multilingual doctor–patient chat**, **AI-powered symptom checker**, **speech-to-text with translation**, and **patient profiles**.

---

## ✨ Features
- **Doctor–Patient Chat** (WhatsApp-style) with multilingual support
- **Symptom Checker** (Groq AI) with recommendations, safe medicines, and tests
- **Speech-to-Text (STT)** + translation from uploaded or recorded audio (`.mp3`, `.wav`, `.ogg`, `.webm`)
- **Patient Profiles**: stores medical history, allergies, chronic conditions
- **Dashboard**: review past conversations and reports

---

## 🛠️ Tech Stack
- **Backend:** FastAPI + MongoDB + Groq AI
- **Frontend:** Streamlit (Python, Tailwind-like styling with components)
- **AI:** Whisper (speech recognition), GoogleTranslator (multilingual support)
- **Database:** MongoDB (local or Atlas)

---

## 📦 Installation

### 1. Clone repo
```bash
git clone https://github.com/your-username/rural-healthcare-ai.git
cd rural-healthcare-ai
