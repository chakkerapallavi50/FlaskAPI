import streamlit as st
import whisper
import torch
import os
import io
from pydub import AudioSegment
 
# Load Whisper model (tiny, base, small, medium, or large)
def chat_page():
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    MODEL_NAME = "small"  # Change this to "base", "medium", or "large" if needed
    model = whisper.load_model(MODEL_NAME, device=DEVICE)
    
    # Function to convert MP3 to WAV
    def convert_mp3_to_wav(mp3_file):
        audio = AudioSegment.from_mp3(mp3_file)
        wav_io = io.BytesIO()
        audio.export(wav_io, format="wav")
        wav_io.seek(0)
        return wav_io
    
    # Function to transcribe audio using Whisper
    def transcribe_audio(audio_file):
        temp_audio_path = "temp_audio.wav"
        with open(temp_audio_path, "wb") as f:
            f.write(audio_file.read())
    
        result = model.transcribe(temp_audio_path)
        os.remove(temp_audio_path)  # Clean up temp file
        return result["text"]
    
    # Streamlit UI
    st.set_page_config(page_title="Speech to Text (Whisper)", layout="wide")
    st.title("🎙 Speech Recognition using Whisper")
    
    # Upload audio file
    uploaded_file = st.file_uploader("Upload an MP3 or WAV file", type=["mp3", "wav"])
    
    if uploaded_file:
        with st.spinner("Processing audio..."):
            # If the uploaded file is MP3, convert it to WAV first
            if uploaded_file.type == "audio/mpeg":  # MP3 file
                wav_audio = convert_mp3_to_wav(uploaded_file)
            else:  # If it's already WAV
                wav_audio = uploaded_file
    
            # Transcribe the audio (WAV file)
            transcript_text = transcribe_audio(wav_audio)
    
            if transcript_text:
                st.subheader("📝 Transcribed Text")
                st.text_area("Transcription", transcript_text, height=250)
    
                # Download button for TXT file
                st.download_button(
                    label="📥 Download Transcription",
                    data=transcript_text,
                    file_name="transcription.txt",
                    mime="text/plain",
                )
            else:
                st.error("Could not transcribe the audio. Try again!")
    