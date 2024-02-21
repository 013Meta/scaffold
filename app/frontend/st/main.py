import requests
import streamlit as st
from st_audiorec import st_audiorec


# Function to send audio to the backend and get transcription
def transcribe_audio(file_path):
    files = {"file": open(file_path, "rb")}
    response = requests.post("http://localhost:8001/transcribe", files=files)
    return response


# Record or upload audio
wav_audio_data = st_audiorec()

if wav_audio_data is not None:
    st.audio(wav_audio_data, format="audio/wav")
    temp_audio_path = "temp_audio.wav"
    with open(temp_audio_path, "wb") as f:
        f.write(wav_audio_data)

    if "transcription" not in st.session_state or st.button("Transcribe"):
        response = transcribe_audio(temp_audio_path)
        if response.status_code == 200:
            transcription = response.json().get(
                "transcription", "No transcription found."
            )
            st.session_state["transcription"] = transcription
            st.text(f"Transcription: {transcription}")
        else:
            st.error("Failed to transcribe audio.")
    else:
        st.text(f"Transcription: {st.session_state['transcription']}")
