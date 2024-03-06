import hmac
from pathlib import Path

import pandas as pd
import streamlit as st
from openai import AzureOpenAI


client = AzureOpenAI(api_key=st.secrets["SONIC_API_KEY"],
                     azure_endpoint=st.secrets["SONIC_ENDPOINT"],
                     api_version="2024-02-15-preview")

def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False
    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True
    # Show input for password.
    st.text_input(
        "Password 🔒", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False

def text_to_speech(text, voice):
    speech_file_path = Path("audio.mp3")
    response = client.audio.speech.create(
      model="tts-hd",
      voice=voice,
      input=text
    )
    response.stream_to_file(speech_file_path)

def speech_to_text(audio_file, include_time_stamp = False, language="en"):
    if include_time_stamp:
        transcription = client.audio.transcriptions.create(
            file=audio_file,
            language=language,
            model="whisper",
            response_format="verbose_json",
            timestamp_granularities=["segment"]
        )

        df = pd.DataFrame(transcription.segments)
        df = df[["start", "end", "text"]]
    
        return df, transcription.text
    
    else:
        transcription = client.audio.transcriptions.create(
            file=audio_file,
            language=language,
            model="whisper"
            )
        return transcription.text
