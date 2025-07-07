# 📝 AI Meeting Minutes

Automatically transcribe, diarize, summarize, and extract action items from meetings—then export everything to a professional PDF report. Ideal for teams and organizations wanting to automate their meeting documentation workflow.

---

## 🚀 Features

- 🎙️ **Audio Transcription** using OpenAI Whisper (local)
- 🧍‍♂️🧍‍♀️ **Speaker Diarization** with pyannote.audio (local)
- 📝 **Summarization** (abstractive & extractive) using Hugging Face and local LLMs (e.g., Mistral)
- ✅ **Action Item Extraction** from transcript (local LLM)
- 📄 **PDF Report Generation**
- 📥 **Google Drive Integration** for downloading large models

---

## 📁 Project Structure

```
ai_meeting_minutes/
├── input/
│   └── download_models.py        # Script to auto-download models from Google Drive
├── output/
│   ├── diarized_transcripts/     # Speaker-attributed transcripts
│   ├── summaries/                # Generated summaries
│   ├── action_items/             # Key action items extracted
│   └── reports/                  # Final PDF reports
├── src/
│   ├── transcription/            # Whisper-based transcription
│   ├── diarization/              # Pyannote-based diarization
│   ├── summarization/            # Summarization logic
│   ├── action_extraction/        # Action item NLP logic
│   └── report/                   # PDF export tools
├── scripts/
│   └── download_models.py        # Helper script for model setup
├── requirements.txt
└── README.md
```

---

## 🛠️ Installation

1. **Clone the repo**
    ```bash
    git clone https://github.com/santhosh-xx/ai-meeting-minutes.git
    cd ai-meeting-minutes
    ```

2. **(Recommended) Create a virtual environment**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Download required models**
    ```bash
    python scripts/download_models.py
    ```
    > **Note:** Large model files are hosted externally (Google Drive). The script will download and unzip them automatically.

---

## ⚡ Quick Start

1. **Place your audio files** in `input/audio/` (supported: WAV, MP3, etc).
2. **Transcribe audio**
    ```bash
    python src/transcription/transcribe_chunked.py <your_audio_file.wav>
    ```
3. **Speaker diarization**
    ```bash
    python src/diarization/transcribe_diarized_chunked.py <your_audio_file.wav>
    ```
4. **Summarization**
    ```bash
    python src/summarization/summarize.py <base_filename>
    ```
    or for diarized output:
    ```bash
    python src/summarization/summarize_diarized.py <base_filename>
    ```
5. **Action item extraction**
    ```bash
    python src/action_extraction/extract_actions.py <base_filename>
    ```
    or for diarized output:
    ```bash
    python src/action_extraction/extract_actions_diarized.py <diarized_transcript_filename>
    ```
6. **PDF report generation**
    - (Script coming soon, or check `src/report/`)

---

## 🧠 Stack

- **Python** 3.8+
- **Audio Processing**: [pydub](https://pydub.com/)
- **Transcription**: [OpenAI Whisper](https://github.com/openai/whisper)
- **Speaker Diarization**: [pyannote.audio](https://github.com/pyannote/pyannote-audio)
- **Summarization**: [transformers](https://github.com/huggingface/transformers) (`distilbart-cnn-12-6`), [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) (local LLMs like Mistral)
- **Action Extraction**: Prompted LLM (Mistral, llama-cpp)
- **PDF Reports**: (e.g., ReportLab, add details as implemented)
- **Google Drive API**: For large model downloads

---

## ⚙️ Configuration

- Model paths, chunk sizes, and other settings can be adjusted in each script or centralized in a `config.yaml` (recommended for advanced users).
- **Environment variables**: Some scripts require Hugging Face tokens (`HF_TOKEN`) for pyannote.

---

## 🧪 Testing & Development

- For development dependencies, linting, and testing, consider adding a `requirements-dev.txt` with:
    - `pytest`
    - `flake8` or `black`
    - `pre-commit`

---

## 📋 Troubleshooting

- **CUDA/CPU support**: Whisper and pyannote support GPU acceleration if available.
- **Large models**: Ensure sufficient disk space and RAM (Mistral 7B GGUF ~4GB RAM minimum).
- **Google Drive quota**: If model downloads fail, check your network and Google Drive limits.
- **Missing dependencies**: Run `pip install -r requirements.txt` inside your virtual environment.

---

## 🤝 Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🙋 FAQ

- **Q:** Can I use my own LLMs or models?
  - **A:** Yes! Place your GGUF/Whisper models in the appropriate input/model folders and update the config or script paths.

- **Q:** Does it work offline?
  - **A:** Yes, after downloading models, all processing is local.

- **Q:** Can I process non-English audio?
  - **A:** Whisper supports multilingual audio; diarization and LLM summarization may need further adaptation.

---

## 🌟 Acknowledgements

- OpenAI for Whisper
- Hugging Face
- pyannote.audio team
- Llama-cpp-python contributors

---

**Automate your meeting minutes—focus on collaboration, not note-taking!**
