from dotenv import load_dotenv
load_dotenv()

import os
from gtts import gTTS
from pydub import AudioSegment
import platform
import subprocess
import elevenlabs  # pip install elevenlabs
import shutil

# ---------- FFmpeg setup for pydub (Windows) ----------
# Adjust paths to your actual ffmpeg.exe and ffprobe.exe
AudioSegment.converter = r"C:\\ffmpeg\\bin\\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\\ffmpeg\\bin\\ffprobe.exe"

# ---------- ElevenLabs API key ----------
ELEVENLABS_API_KEY = os.environ.get("ELEVEN_API_KEY")
if ELEVENLABS_API_KEY:
    elevenlabs.set_api_key(ELEVENLABS_API_KEY)
else:
    print("Warning: ELEVEN_API_KEY not found in environment variables.")

# ---------- Audio playback helper ----------
def _play_audio(filepath):
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', filepath])
        elif os_name == "Windows":  # Windows
            wav_path = filepath.replace(".mp3", ".wav")
            audio = AudioSegment.from_mp3(filepath)
            audio.export(wav_path, format="wav")
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_path}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', filepath])
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"Error playing audio: {e}")

# ---------- gTTS functions ----------
def text_to_speech_with_gtts(input_text, output_filepath):
    tts = gTTS(text=input_text, lang="en", slow=False)
    tts.save(output_filepath)
    _play_audio(output_filepath)

# ---------- ElevenLabs functions ----------
def text_to_speech_with_elevenlabs(input_text, output_filepath):
    audio = elevenlabs.generate(
        text=input_text,
        voice="Aria",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2"
    )
    with open(output_filepath, "wb") as f:
        f.write(audio)
    _play_audio(output_filepath)

# ---------- Example usage ----------
if __name__ == "__main__":
    text = "Hi this is saniya , autoplay testing!"
    text_to_speech_with_gtts(text, "gtts_test.mp3")
    # To test ElevenLabs, first set your ELEVEN_API_KEY in .env, then uncomment:
    # text_to_speech_with_elevenlabs(text, "elevenlabs_test.mp3")
