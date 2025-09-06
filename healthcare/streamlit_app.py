# app.py (Streamlit Frontend)
import streamlit as st
import requests
import json

# -------------------------------
# Backend API Base URL
# -------------------------------
API_URL = "http://127.0.0.1:8000"  # change if backend is remote

# -------------------------------
# Streamlit Config
# -------------------------------
st.set_page_config(page_title="Rural Healthcare", page_icon="🩺", layout="wide")
st.title("🩺 Rural Healthcare Web App")

# -------------------------------
# Sidebar Navigation
# -------------------------------
menu = st.sidebar.radio(
    "Navigation",
    ["Chat", "Symptom Checker", "Audio STT + Translation", "Patient Dashboard"]
)

# -------------------------------
# Chat Page
# -------------------------------
if menu == "Chat":
    st.header("💬 Doctor–Patient Chat")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    conversation_id = st.text_input("Conversation ID", value="conv001")

    # Show chat history
    for msg in st.session_state.chat_history:
        role = "🧑 Patient" if msg["role"] == "patient" else "👨‍⚕️ Doctor"
        st.markdown(f"**{role}:** {msg['text']}")

    # Input box
    user_input = st.text_input("Type your message:")
    if st.button("Send"):
        if user_input.strip():
            payload = {
                "conversation_id": conversation_id,
                "message": user_input,
                "source_lang": "auto",
                "target_lang": "en",
            }
            response = requests.post(f"{API_URL}/chat/", json=payload)
            if response.status_code == 200:
                result = response.json()
                st.session_state.chat_history = result["history"]
            else:
                st.error(f"Error: {response.text}")

# -------------------------------
# Symptom Checker Page
# -------------------------------
elif menu == "Symptom Checker":
    st.header("🩺 AI Symptom Checker")

    conversation_id = st.text_input("Conversation ID", value="conv001")
    text = st.text_area("Describe your symptoms:")
    age = st.number_input("Age", min_value=1, max_value=120, value=30)
    sex = st.selectbox("Sex", ["male", "female", "other"])

    if st.button("Analyze Symptoms"):
        payload = {
            "conversation_id": conversation_id,
            "text": text,
            "age": age,
            "sex": sex,
        }
        response = requests.post(f"{API_URL}/symptom-check/", json=payload)
        if response.status_code == 200:
            result = response.json()
            st.subheader("Summary")
            st.write(result["summary"])

            st.subheader("Probable Conditions")
            st.write(result["probable_conditions"])

            st.subheader("Recommendations")
            st.write(result["recommendations"])

            if result.get("recommended_tests"):
                st.subheader("Recommended Tests")
                st.write(result["recommended_tests"])

            if result.get("recommended_medicines"):
                st.subheader("Recommended Medicines")
                st.write(result["recommended_medicines"])
        else:
            st.error(f"Error: {response.text}")

# -------------------------------
# Audio STT + Translation Page
# -------------------------------
elif menu == "Audio STT + Translation":
    st.header("🎤 Upload Audio (STT + Translation)")

    conversation_id = st.text_input("Conversation ID", value="conv001")
    target_lang = st.selectbox("Translate To", ["en", "hi", "pa", "bn", "te", "ta"])

    uploaded_file = st.file_uploader("Upload audio file", type=["mp3", "wav", "ogg", "webm"])
    if uploaded_file is not None:
        st.audio(uploaded_file, format="audio/mp3")

        if st.button("Transcribe & Translate"):
            files = {"file": uploaded_file.getvalue()}
            response = requests.post(
                f"{API_URL}/stt-translate/?target_lang={target_lang}",
                files={"file": (uploaded_file.name, uploaded_file, uploaded_file.type)},
            )
            if response.status_code == 200:
                result = response.json()
                st.success("✅ Transcription Complete")
                st.write(f"**Original:** {result['original_text']}")
                st.write(f"**Translated ({target_lang}):** {result['translated_text']}")
            else:
                st.error(f"Error: {response.text}")

# -------------------------------
# Patient Dashboard Page
# -------------------------------
elif menu == "Patient Dashboard":
    st.header("📊 Patient Dashboard")

    patient_id = st.text_input("Enter Patient ID", value="patient001")

    if st.button("Fetch Patient Profile"):
        response = requests.get(f"{API_URL}/patients/{patient_id}")
        if response.status_code == 200:
            profile = response.json()
            st.subheader("👤 Patient Profile")
            st.json(profile)
        else:
            st.error("❌ Patient not found")

    conversation_id = st.text_input("Conversation ID (for history)", value="conv001")

    if st.button("Fetch Conversation History"):
        response = requests.get(f"{API_URL}/chat/{conversation_id}")
        if response.status_code == 200:
            history = response.json()
            st.subheader("💬 Conversation History")
            for msg in history["history"]:
                role = "🧑 Patient" if msg["role"] == "patient" else "👨‍⚕️ Doctor"
                st.markdown(f"**{role}:** {msg['text']}")
        else:
            st.error("❌ No conversation found")
