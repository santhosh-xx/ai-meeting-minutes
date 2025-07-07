
# 🧠 AI Meeting Minutes

Automated meeting understanding pipeline — transcribes audio, performs speaker diarization, extracts action items, generates summaries, and exports everything into a neat PDF report. No more manually writing minutes!

---

## 🚀 Features

- 🎙️ **Audio Transcription** using OpenAI Whisper
- 🧍‍♂️🧍‍♀️ **Speaker Diarization** (who said what?)
- 📝 **Summary Generation** (abstract & extractive)
- ✅ **Action Item Extraction**
- 📄 **PDF Report Export** (with highlights)
- 📥 **Google Drive Integration** for model download

---

## 📁 Project Structure

ai_meeting_minutes/
├── input/
│ └── download_models.py # Auto-download model ZIP from Google Drive
├── output/
│ ├── diarized_transcripts/ # Speaker-wise text
│ ├── summaries/ # Generated summaries
│ ├── action_items/ # Key tasks extracted
│ └── reports/ # Final PDF reports
├── src/
│ ├── transcription/ # Whisper-based transcription
│ ├── diarization/ # Pyannote-style diarization
│ ├── summarization/ # Summarization logic
│ ├── action_extraction/ # Action item NLP logic
│ └── report/ # PDF export tools
├── scripts/
│ └── download_models.py # Downloads zipped models from Google Drive
├── requirements.txt
└── README.md


---

## 🛠️ Installation

1. **Clone the repo**

git clone https://github.com/santhosh-xx/ai-meeting-minutes.git
cd ai-meeting-minutes

2. Create virtual environment (optional but recommended)

python -m venv venv
venv\Scripts\activate  # on Windows
source venv/bin/activate  # on Mac/Linux

3. Install dependencies

pip install -r requirements.txt

4. Download required models

python download_models.py


**🧠 Model Download (Google Drive)**
Large model files are hosted externally (not pushed to GitHub).
The script will automatically download and unzip them from Google Drive.



