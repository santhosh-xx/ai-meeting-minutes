import sys
import logging
import textwrap
from pathlib import Path
from llama_cpp import Llama

# ------------------ CONFIG ------------------

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "input" / "models" / "mistral-7b-instruct-v0.3-gguf" / "mistral-7b-instruct-v0.3.Q4_K_M.gguf"
INPUT_DIR = BASE_DIR / "output" / "diarized_transcripts"
OUTPUT_DIR = BASE_DIR / "output" / "action_items"
MAX_CHARS_PER_CHUNK = 3500

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# ------------------ INPUT CHECK ------------------

if len(sys.argv) < 2:
    logging.error("❌ Usage: python extract_actions_diarized.py <diarized_transcript_filename>")
    sys.exit(1)

input_filename = sys.argv[1]
input_path = INPUT_DIR / input_filename

if not input_path.exists():
    logging.error(f"❌ File not found: {input_path}")
    sys.exit(1)

base_name = input_path.stem.replace("_diarized", "")
output_path = OUTPUT_DIR / f"{base_name}_action_items.txt"

# ------------------ LOAD MODEL ------------------

if not MODEL_PATH.exists():
    logging.error(f"❌ Model not found: {MODEL_PATH}")
    sys.exit(1)

logging.info("🧠 Loading local Mistral model via llama-cpp...")
llm = Llama(
    model_path=str(MODEL_PATH),
    n_ctx=4096,
    n_threads=8,
    n_batch=512,
    temperature=0.3,
    stop=["</s>"],
    verbose=False
)

# ------------------ READ INPUT ------------------

transcript = input_path.read_text(encoding="utf-8")
logging.info(f"📄 Loaded transcript: {len(transcript)} characters")

# ------------------ CHUNKING ------------------

chunks = textwrap.wrap(transcript, MAX_CHARS_PER_CHUNK, break_long_words=False, break_on_hyphens=False)
logging.info(f"✂️ Split transcript into {len(chunks)} chunk(s)")

# ------------------ PROMPT TEMPLATE ------------------

def format_prompt(text):
    return f"""### Meeting Transcript:
{text}

### Instruction:
From the above transcript, extract all actionable items discussed by the speakers.

For each action item, include:
- Task description
- Assigned speaker (e.g., Speaker_1)
- Deadline or time if mentioned

### Format:
- Speaker_X: Do <task> [by <deadline> if any]

### Action Items:
"""

# ------------------ EXTRACT ACTIONS ------------------

action_items = []

for idx, chunk in enumerate(chunks):
    logging.info(f"📌 Extracting from chunk {idx+1}/{len(chunks)}...")
    prompt = format_prompt(chunk)
    response = llm(prompt, max_tokens=1024)

    if isinstance(response, dict) and "choices" in response:
        output_text = response["choices"][0]["text"].strip()
    else:
        output_text = response.strip()

    action_items.append(f"🔹 Chunk {idx+1}:\n{output_text}\n")

# ------------------ SAVE OUTPUT ------------------

output_path.write_text("\n".join(action_items), encoding="utf-8")
logging.info(f"✅ Done! Action items saved to: {output_path}")
