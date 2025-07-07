import os
import sys
from math import ceil
from pathlib import Path
from pydub import AudioSegment
import whisper

# ----- Constants -----

AUDIO_DIR = Path("../../input/audio") 
CHUNK_OUTPUT_DIR = Path("../../output/audio_chunks")  
OUTPUT_DIR = Path("../../output/transcripts")         
CHUNK_LENGTH_MS = 10 * 60 * 1000  

os.makedirs(CHUNK_OUTPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ----- Split audio into chunks -----

def split_audio(audio_path):
    ext = audio_path.suffix.lower().replace(".", "")
    try:
        audio = AudioSegment.from_file(audio_path, format=ext)
    except Exception as e:
        print(f"❌ Failed to load audio file: {e}")
        sys.exit(1)

    total_duration_sec = len(audio) // 1000
    mins, secs = divmod(total_duration_sec, 60)
    num_chunks = ceil(len(audio) / CHUNK_LENGTH_MS)

    print(f"📊 Audio Duration: {mins} min {secs} sec")
    print(f"🔪 Chunking into {num_chunks} chunk(s) of {CHUNK_LENGTH_MS // 60000} min each...")

    chunks = []
    chunk_folder = CHUNK_OUTPUT_DIR / f"{audio_path.stem}_chunks"
    os.makedirs(chunk_folder, exist_ok=True)

    for i in range(num_chunks):
        chunk = audio[i * CHUNK_LENGTH_MS: (i + 1) * CHUNK_LENGTH_MS]
        chunk_path = chunk_folder / f"{audio_path.stem}_chunk{i}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)

    return chunks

# ----- Transcribe chunks using Whisper -----

def transcribe_chunks(chunk_paths, model_name="base"):
    model = whisper.load_model(model_name)
    all_text = ""
    for i, chunk_path in enumerate(chunk_paths):
        print(f"🔍 Transcribing chunk {i+1}/{len(chunk_paths)}: {chunk_path.name}")
        result = model.transcribe(str(chunk_path))
        all_text += f"\n--- Chunk {i+1} ---\n{result['text'].strip()}\n"
        os.remove(chunk_path)  
    return all_text.strip()

# ----- Main -----

def main(filename):
    audio_path = AUDIO_DIR / filename
    if not audio_path.exists():
        print(f"❌ Audio file not found: {audio_path}")
        sys.exit(1)

    base_name = audio_path.stem
    output_folder = OUTPUT_DIR / f"{base_name}_transcripts"
    os.makedirs(output_folder, exist_ok=True)
    output_path = output_folder / f"{base_name}_transcript.txt"

    print(f"🔄 Splitting audio: {filename}")
    chunk_paths = split_audio(audio_path)

    print(f"🧠 Transcribing {len(chunk_paths)} chunks...")
    full_transcript = transcribe_chunks(chunk_paths)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_transcript)

    print(f"✅ Transcript saved to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transcribe_chunked.py <audio_filename>")
    else:
        main(sys.argv[1])
