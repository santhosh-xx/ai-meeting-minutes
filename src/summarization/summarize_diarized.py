# src/summarization/summarize_diarized.py

import os
import textwrap
import logging
import argparse
from pathlib import Path
from llama_cpp import Llama

# ------------------ LOGGING ------------------

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

# ------------------ CONFIG ------------------

BASE_DIR = Path(__file__).resolve().parents[2]
TRANSCRIPT_DIR = BASE_DIR / "output" / "diarized_transcripts"
OUTPUT_DIR = BASE_DIR / "output" / "summaries"
MODEL_PATH = BASE_DIR / "input" / "models" / "mistral-7b-instruct-v0.3-gguf" / "mistral-7b-instruct-v0.3.Q4_K_M.gguf"

MAX_CHARS_PER_CHUNK = 3500
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ------------------ PROMPT TEMPLATE ------------------

def format_prompt(text):
    return f"""### Transcript:
{text}

### Instruction:
Summarize this meeting segment. Group content by each speaker. Include:
- Topics discussed
- Key points per speaker
- Decisions made (if any)

### Summary:
"""

# ------------------ SUMMARIZER ------------------

def summarize_diarized_transcript(input_path: Path, output_path: Path):
    transcript = input_path.read_text(encoding="utf-8")
    log.info(f"📄 Loaded transcript: {len(transcript)} characters")

    # Chunk transcript

    chunks = textwrap.wrap(transcript, MAX_CHARS_PER_CHUNK, break_long_words=False, break_on_hyphens=False)
    log.info(f"✂️ Split transcript into {len(chunks)} chunk(s)")

    # Load model

    log.info("🧠 Loading local Mistral model via llama-cpp...")
    llm = Llama(
        model_path=str(MODEL_PATH),
        n_ctx=4096,
        n_threads=8,
        n_batch=512,
        temperature=0.3,
        stop=["</s>"],
        verbose=False
    )

    final_summary = []
    for idx, chunk in enumerate(chunks):
        log.info(f"📝 Summarizing chunk {idx + 1}/{len(chunks)}...")
        prompt = format_prompt(chunk)
        response = llm(prompt, max_tokens=1024)

        if isinstance(response, dict) and "choices" in response:
            output_text = response["choices"][0]["text"].strip()
        else:
            output_text = "[⚠️ LLM failed to generate valid output]"

        final_summary.append(f"🔹 Chunk {idx+1} Summary:\n{output_text}\n")

    output_path.write_text("\n".join(final_summary), encoding="utf-8")
    log.info(f"✅ Done! Summary saved to: {output_path}")

# ------------------ ENTRY POINT ------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Summarize a diarized transcript")
    parser.add_argument("filename", help="Diarized transcript filename (e.g., sample_diarized.txt)")
    args = parser.parse_args()

    input_path = TRANSCRIPT_DIR / args.filename
    if not input_path.exists():
        log.error(f"❌ File not found: {input_path}")
        exit(1)

    base_name = args.filename.replace("_diarized", "")
    output_path = OUTPUT_DIR / f"{base_name}_summary.txt"

    summarize_diarized_transcript(input_path, output_path)
