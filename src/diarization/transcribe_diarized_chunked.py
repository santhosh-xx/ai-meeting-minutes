import os
import sys
import whisper
from tempfile import NamedTemporaryFile
from pydub import AudioSegment
from pyannote.audio import Pipeline
from pyannote.core import Segment
from pathlib import Path

# ------------------ CONFIG ------------------

INPUT_DIR = Path("../../input/audio")
OUTPUT_DIR = Path("../../output/diarized_transcripts")
WHISPER_MODEL = "base"
CHUNK_LENGTH_MS = 5 * 60 * 1000  
HF_TOKEN = os.getenv("HF_TOKEN", None)
PYANNOTE_MODEL_ID = "pyannote/speaker-diarization-3.1"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ------------------ HELPER: Find file ------------------

def find_file(filename: str, search_path: Path) -> Path:
    files_found = list(search_path.rglob(filename))
    if files_found:
        return files_found[0]
    return None

# ------------------ CHECK ARGS ------------------

if len(sys.argv) < 2:
    print("\u274c Usage: python transcribe_diarized_chunked.py <audio_filename>")
    sys.exit(1)

filename = sys.argv[1]

print(f"🔍 Searching for '{filename}' inside '{INPUT_DIR}'...")
audio_path = find_file(filename, INPUT_DIR)

if audio_path is None or not audio_path.exists():
    print(f"❌ File not found: {INPUT_DIR / filename}")
    sys.exit(1)

print(f"✅ Found audio file at: {audio_path}")

base_name = audio_path.stem

# ------------------ LOAD MODELS ------------------

print("🔁 Loading Whisper and PyAnnote models...")
whisper_model = whisper.load_model(WHISPER_MODEL)
pipeline = Pipeline.from_pretrained(PYANNOTE_MODEL_ID, use_auth_token=HF_TOKEN)

# ------------------ SPLIT AUDIO ------------------

print("🎧 Loading audio and splitting into 5-minute chunks...")
audio = AudioSegment.from_file(audio_path)
duration_ms = len(audio)
chunk_count = (duration_ms + CHUNK_LENGTH_MS - 1) // CHUNK_LENGTH_MS
print(f"🕒 Total duration: {duration_ms / 60000:.2f} min | Chunks: {chunk_count}")

all_segments = []

for i in range(chunk_count):
    chunk_start_ms = i * CHUNK_LENGTH_MS
    chunk = audio[chunk_start_ms:chunk_start_ms + CHUNK_LENGTH_MS]

    with NamedTemporaryFile(suffix=".wav", delete=False) as chunk_wav:
        
        chunk.set_channels(1).set_frame_rate(16000).export(chunk_wav.name, format="wav")
        chunk_path = chunk_wav.name

    print(f"🧠 Chunk {i+1}/{chunk_count}: Performing speaker diarization...")
    diarization = pipeline(chunk_path)

    print(f"✍️ Chunk {i+1}/{chunk_count}: Transcribing with Whisper...")
    whisper_result = whisper_model.transcribe(chunk_path, language="en", fp16=False)
    segments = whisper_result["segments"]

    for segment in segments:
        start = segment["start"]
        end = segment["end"]
        text = segment["text"]
        global_start = chunk_start_ms / 1000 + start
        global_end = chunk_start_ms / 1000 + end

        diarization_seg = Segment(start, end)
        speaker_label = diarization.crop(diarization_seg).labels()

        assigned_speaker = speaker_label[0] if speaker_label else "Unknown"

        all_segments.append((global_start, global_end, assigned_speaker, text.strip()))

    # Clean up temporary chunk file
    os.remove(chunk_path)

# ------------------ SAVE OUTPUT ------------------

print("🗾 Saving final diarized transcript...")
all_segments.sort(key=lambda x: x[0])

output_lines = [
    f"{speaker} [{start:.2f} - {end:.2f}]: {text}"
    for start, end, speaker, text in all_segments
]

output_path = OUTPUT_DIR / f"{base_name}_diarized.txt"
with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

print(f"✅ Done! Diarized transcript saved to: {output_path}")
