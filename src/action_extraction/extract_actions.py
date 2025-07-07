import os
import sys
import argparse
import logging
from pathlib import Path
from llama_cpp import Llama

# ------------------ CONFIG ------------------

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "input" / "models" / "mistral-7b-instruct-v0.3-gguf" / "mistral-7b-instruct-v0.3.Q4_K_M.gguf"
INPUT_DIR = BASE_DIR / "output" / "transcripts"
OUTPUT_DIR = BASE_DIR / "output" / "action_items"
CHUNK_CHAR_LENGTH = 3000
MAX_TOKENS = 512

# ------------------ SETUP ------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# ------------------ UTILS ------------------

def chunk_text(text, max_chars):
    return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]

def build_prompt(transcript_chunk):
    return f"""
You are an expert AI meeting assistant.

Extract clear and concise ACTION ITEMS from the following meeting transcript chunk.

Each action item should follow this format:
✅ Action Item: [What needs to be done]
   - 🙋 Assigned to: [Person] (if known)
   - 📅 Deadline: [Date/Time] (if mentioned)

Transcript:
\"\"\" 
{transcript_chunk} 
\"\"\"

Respond ONLY with the formatted action items, no explanations.
"""

def extract_action_items(llm, transcript_text):
    chunks = chunk_text(transcript_text, CHUNK_CHAR_LENGTH)
    action_items = []

    for idx, chunk in enumerate(chunks):
        logging.info(f"⚙️ Extracting from chunk {idx + 1}/{len(chunks)}...")
        prompt = build_prompt(chunk)
        response = llm(prompt, max_tokens=MAX_TOKENS)

        result = response["choices"][0]["text"].strip() if isinstance(response, dict) else response.strip()
        action_items.append(result)

    return "\n\n".join(action_items)

# ------------------ MAIN ------------------

def main(base_filename):
    input_path = INPUT_DIR / f"{base_filename}_transcripts" / f"{base_filename}_transcript.txt"
    output_path = OUTPUT_DIR / f"{base_filename}_action_items.txt"

    if not input_path.exists():
        logging.error(f"❌ Transcript not found: {input_path}")
        sys.exit(1)

    transcript_text = input_path.read_text(encoding="utf-8")

    if not MODEL_PATH.exists():
        logging.error(f"❌ Model file not found: {MODEL_PATH}")
        sys.exit(1)

    logging.info(f"🔄 Loading GGUF model from: {MODEL_PATH}")
    llm = Llama(
        model_path=str(MODEL_PATH),
        n_ctx=4096,
        n_threads=6,
        verbose=False
    )

    logging.info(f"📄 Processing transcript: {base_filename}")
    extracted = extract_action_items(llm, transcript_text)

    output_path.write_text(extracted, encoding="utf-8")
    logging.info(f"✅ Action items saved to: {output_path}")

# ------------------ ENTRY ------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract action items from transcript.")
    parser.add_argument("filename", help="Base filename without extension")
    args = parser.parse_args()

    main(args.filename)
