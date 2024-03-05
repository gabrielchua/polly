"""
app.py
"""
import streamlit as st

from utils import (
    check_password,
    text_to_speech,
    speech_to_text
)

VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

st.set_page_config(page_title="Polly",
                   page_icon="🦜")

if not check_password():
    st.stop()

st.title("Polly 🦜")

tab1, tab2 = st.tabs(["Text to Speech", "Speech to Text"])

with tab1:
    st.warning(st.secrets["tts_disclaimer"], icon="🚨")
    text = st.text_area("Enter text", "Hello, how are you?")
    voice = st.radio("Voice", VOICES, horizontal = True)
    st.write("🎙️ You can find a demo of these voices [here](https://platform.openai.com/docs/guides/text-to-speech/voice-options).")
    if text is not None:
        if st.button("Generate"):
            with st.spinner("Generating audio - this takes about 20 to 30 seconds..."):
                try:
                    text_to_speech(text, voice)
                except:
                    st.warning("Unexpected error occurred. Please try again in ~ 1 minute.", icon="⚠️")
                    st.stop()
            audio_file = open("audio.mp3", 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/mpeg')
            st.download_button(label="Download",
                                data=audio_bytes,
                                file_name="audio.mp3",
                                mime="audio/mp3")

with tab2:
    st.warning(st.secrets["stt_disclaimer"], icon="🚨")
    audio_file = st.file_uploader("Upload audio file", type=["mp3", "wav"])
    # language = st.radio("Language", list(LANGUAGES.keys()), horizontal = True)
    if audio_file is not None:
        if st.button("Transcribe"):
            with st.spinner("Transcribing audio - this takes about 20 to 30 seconds..."):
                try:
                    transcription = speech_to_text(audio_file)
                except:
                    st.warning("Unexpected error occurred. Please try again in ~ 1 minute.", icon="⚠️")
                    st.stop()
            st.write(transcription)
