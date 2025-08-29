import os
import json
import queue
import sounddevice as sd
import gradio as gr
from vosk import Model, KaldiRecognizer
from gtts import gTTS
import subprocess
from pathlib import Path
import shutil
import numpy as np
from scipy.signal import resample

# ----------------------------
# Paths and setup
# ----------------------------
ROOT = Path(__file__).parent
MODEL_DIR = ROOT / "models"
EN_MODEL_PATH = MODEL_DIR / "vosk-model-small-en-us-0.15"
HI_MODEL_PATH = MODEL_DIR / "vosk-model-small-hi-0.22"
OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# ----------------------------
# Ollama path detection
# ----------------------------
DEFAULT_OLLAMA_PATH = Path(r"C:\Users\tejas\AppData\Local\Programs\Ollama\ollama.exe")
OLLAMA_PATH = shutil.which("ollama")  # Try to find in PATH first
if OLLAMA_PATH:
    OLLAMA_PATH = Path(OLLAMA_PATH)
else:
    OLLAMA_PATH = DEFAULT_OLLAMA_PATH

# ----------------------------
# Audio resampling function
# ----------------------------
def resample_audio(audio_bytes, original_rate=48000, target_rate=16000):
    audio_np = np.frombuffer(audio_bytes, dtype=np.int16)
    num_samples = int(len(audio_np) * target_rate / original_rate)
    audio_resampled = resample(audio_np, num_samples)
    return audio_resampled.astype(np.int16).tobytes()

# ----------------------------
# Speech to Text (Vosk)
# ----------------------------
def record_and_transcribe(language="en", duration=5, mic_rate=48000, target_rate=16000):
    model_path = HI_MODEL_PATH if language == "hi" else EN_MODEL_PATH
    if not model_path.exists():
        raise FileNotFoundError(f"Vosk model for {language} not found in {model_path}")
    model = Model(str(model_path))
    
    recognizer = KaldiRecognizer(model, target_rate)
    recognizer.SetWords(True)

    q = queue.Queue()

    def callback(indata, frames, time, status):
        if status:
            print(status)
        q.put(bytes(indata))

    with sd.RawInputStream(samplerate=mic_rate, blocksize=8000,
                           dtype='int16', channels=1, callback=callback):
        print("Recording...")
        audio_data = bytes()
        for _ in range(int(duration * mic_rate / 8000)):
            audio_data += q.get()
        print("Done recording.")

    audio_data = resample_audio(audio_data, original_rate=mic_rate, target_rate=target_rate)
    recognizer.AcceptWaveform(audio_data)
    result = recognizer.Result()
    text = json.loads(result).get("text", "")
    return text.strip()

# ----------------------------
# LLaMA 3.1 via Ollama
# ----------------------------
def generate_story(prompt, model="llama3.1"):
    if not OLLAMA_PATH.exists():
        return "Error: Ollama executable not found. Please check the installation path."
    
    try:
        result = subprocess.run(
            [str(OLLAMA_PATH), "run", model],
            input=prompt,       # send string, not bytes
            capture_output=True,
            text=True,          # text mode
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error generating story: {e.stderr}"

# ----------------------------
# Text to Speech (gTTS)
# ----------------------------
def text_to_speech(text, lang="en", tld="com"):
    tts = gTTS(text=text, lang=lang, tld=tld)
    output_path = OUTPUT_DIR / "story.mp3"
    tts.save(output_path)
    return str(output_path)

# ----------------------------
# Gradio App logic
# ----------------------------
def storyteller(language, duration, typed_text):
    # Use typed text if provided, otherwise record speech
    if typed_text and typed_text.strip():
        transcript = typed_text.strip()
    else:
        transcript = record_and_transcribe(language=language, duration=duration)
        if not transcript:
            return "No speech detected", None, None

    story = generate_story(f"Tell me a story about: {transcript}")

    if language == "hi":
        audio_path = text_to_speech(story, lang="hi", tld="co.in")
    else:
        audio_path = text_to_speech(story, lang="en", tld="com")

    return transcript, story, audio_path

# ----------------------------
# Gradio UI
# ----------------------------
with gr.Blocks() as demo:
    gr.Markdown("## 🎙️ Personal Storyteller with LLaMA 3.1 (English & Hindi)\nYou can type your prompt or speak to generate a story.")

    language = gr.Radio(["en", "hi"], value="en", label="Language (en = English, hi = Hindi)")
    duration = gr.Slider(3, 10, value=5, step=1, label="Recording duration (seconds)")
    typed_text = gr.Textbox(label="Or type your story prompt here", placeholder="Type something instead of speaking...")

    btn = gr.Button("🎤 Record & Tell Story")

    transcript = gr.Textbox(label="Transcript / Input")
    story = gr.Textbox(label="Generated Story")
    audio = gr.Audio(label="Story Audio", type="filepath")

    btn.click(fn=storyteller, inputs=[language, duration, typed_text], outputs=[transcript, story, audio])

if __name__ == "__main__":
    demo.launch(share=True)
