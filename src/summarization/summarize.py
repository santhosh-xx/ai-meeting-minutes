from transformers import pipeline
import os
import sys
import textwrap
import logging
import argparse

# ------------------ CONFIG ------------------

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TRANSCRIPT_DIR = os.path.join(BASE_DIR, "output", "transcripts")
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "summary")
CHUNK_TOKEN_LIMIT = 900
MODEL_NAME = "sshleifer/distilbart-cnn-12-6"

# ------------------ LOGGING ------------------

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# ------------------ UTILS ------------------

def load_transcript(transcript_path):
    if not os.path.exists(transcript_path):
        raise FileNotFoundError(f"Transcript not found: {transcript_path}")
    with open(transcript_path, "r", encoding="utf-8") as f:
        return f.read()

def chunk_text(text, max_tokens=CHUNK_TOKEN_LIMIT):
    words = text.split()
    for i in range(0, len(words), max_tokens):
        yield " ".join(words[i:i + max_tokens])

def format_summary(summary_text):
    return f"""📝 Meeting Summary

🔹 Key Topics:
{textwrap.fill(summary_text, width=100)}

🔹 Decisions Made:
- [Extract manually or via Module 3]

🔹 Action Items:
- [To be generated in Module 3]
"""

# ------------------ SUMMARIZATION ------------------

def summarize(text):
    logging.info("🔄 Loading summarization pipeline...")
    summarizer = pipeline("summarization", model=MODEL_NAME)

    summaries = []
    logging.info("🧩 Splitting transcript into chunks...")
    for i, chunk in enumerate(chunk_text(text)):
        logging.info(f"→ Summarizing chunk {i + 1}...")
        out = summarizer(chunk, max_length=150, min_length=40, do_sample=False)
        summaries.append(out[0]['summary_text'])

    full_summary = " ".join(summaries)
    return format_summary(full_summary)

# ------------------ MAIN ------------------

def main(filename):
    transcript_path = os.path.join(TRANSCRIPT_DIR, f"{filename}_transcripts", f"{filename}_transcript.txt")
    output_path = os.path.join(OUTPUT_DIR, f"{filename}_summary.txt")

    try:
        transcript = load_transcript(transcript_path)
        final_summary = summarize(transcript)

        os.makedirs(OUTPUT_DIR, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_summary)

        logging.info(f"✅ Summary saved to: {output_path}")
        print("\n--- Final Summary Preview ---\n")
        print(final_summary)

    except Exception as e:
        logging.error(f"❌ Error: {e}")

# ------------------ ENTRY ------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Summarize transcript using Hugging Face distilBART model.")
    parser.add_argument("filename", help="Base filename of transcript (without _transcript.txt)")
    args = parser.parse_args()

    main(args.filename)
