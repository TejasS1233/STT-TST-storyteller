# 🎙️ Personal Storyteller with LLaMA 3.1 (English & Hindi)

Personal Storyteller is a Python application that generates personalized stories using either **voice input** or **typed prompts**. It leverages offline speech recognition with **Vosk**, story generation via **LLaMA 3.1 (Ollama)**, and converts text-to-speech using **gTTS**, all wrapped in a **Gradio web interface** for easy interaction.

---

## 🚀 Features

- **Voice Input**: Record your voice and transcribe it into text offline using Vosk.
- **Text Input**: Optionally type your story prompt.
- **Story Generation**: Generate creative stories with LLaMA 3.1 via Ollama.
- **Text-to-Speech**: Convert generated stories into audio using gTTS.
- **Bilingual Support**: Works with **English** and **Hindi**.
- **Interactive UI**: User-friendly web interface powered by Gradio.

---



## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/personal-storyteller.git
cd personal-storyteller
2. Set up Python environment
Create a virtual environment and activate it:

Linux/Mac:
python -m venv .venv && source .venv/bin/activate

Windows:
python -m venv .venv && .venv\Scripts\activate

Then install dependencies:
```

2.Copy code
```pip install -r requirements.txt```
Dependencies include vosk, sounddevice, gradio, gtts, numpy, scipy.

3. Download Vosk Models
Download the required models from Vosk Models and place them in the models/ folder:

```
vosk-model-small-en-us-0.15 (English)

vosk-model-small-hi-0.22 (Hindi)
```

4. Install Ollama & LLaMA 3.1
Download and install Ollama. Ensure ollama.exe is in your system PATH, or update the path in app.py.

🎯 Usage
Run the application:

bash
Copy code
python app.py
Open the Gradio web interface (usually http://127.0.0.1:7860).

Select language (English or Hindi).

Record your voice or type a prompt.

Click 🎤 Record & Tell Story.

View the transcript, generated story, and play the audio output.
```
📂 Project Structure
bash
Copy code
personal-storyteller/
├── app.py             # Main application script
├── models/            # Vosk language models
├── output/            # Generated audio files  
└── README.md
```
## ⚙️ How It Works
Input: Accepts user voice or typed prompt.

STT (Speech-to-Text): Converts voice to text using Vosk.

Story Generation: LLaMA 3.1 generates a story from the prompt via Ollama.

TTS (Text-to-Speech): Converts generated story to audio using gTTS.

Output: Displays transcript, story text, and audio playback in Gradio.

## 🧰 Key Libraries & Tools
Library	Purpose
vosk	Offline speech recognition
gtts	Text-to-speech
gradio	Interactive web interface
sounddevice	Capture microphone audio
subprocess	Run Ollama CLI for story generation
numpy & scipy	Audio resampling and processing
pathlib & shutil	File handling and path management

## 🤝 Contributing
Contributions are welcome! To contribute:

Fork the repository.

Create a feature branch (git checkout -b feature-name).

Commit your changes (git commit -m "Add feature").

Push to the branch (git push origin feature-name).

Open a Pull Request.

## 📄 License
This project is licensed under the MIT License.
© Tejas
