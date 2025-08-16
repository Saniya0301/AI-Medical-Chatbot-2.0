from dotenv import load_dotenv
load_dotenv()

import os
import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
from groq import Groq

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Audio recording utility
def record_audio(file_path, timeout=20, phrase_time_limit=None):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        logging.info("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        logging.info("Recording...")
        audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        logging.info("Recording complete.")
    # Save to WAV with SpeechRecognition, convert to MP3 with pydub
    wav_data = audio.get_wav_data()
    wav_audio = AudioSegment.from_file(BytesIO(wav_data), format="wav")
    wav_audio.export(file_path, format="mp3")
    logging.info(f"Audio saved to {file_path}")

# Speech-to-text utility using Groq Whisper
def transcribe_with_groq(stt_model, audio_filepath, groq_api_key):
    client = Groq(api_key=groq_api_key)
    with open(audio_filepath, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=file,
            model=stt_model,
            response_format="text"
        )
    return transcription.text

if __name__ == "__main__":
    # Select your filenames and API details
    audio_filepath = "patient_voice_test_for_patient.mp3"
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    stt_model = "whisper-large-v3-turbo"
    
    # 1. Record audio
    record_audio(audio_filepath)  # Remove/comment if you want to use a pre-recorded mp3

    # 2. Transcribe audio (only if the API key is available and file exists)
    if not GROQ_API_KEY:
        logging.error("GROQ_API_KEY not found in environment variables.")
    elif not os.path.exists(audio_filepath):
        logging.error(f"{audio_filepath} does not exist. Record or supply a valid MP3 file.")
    else:
        text = transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY)
        print("Transcription Result:")
        print(text)
