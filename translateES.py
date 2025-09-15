from googletrans import Translator
from langdetect import detect, DetectorFactory
import os

# For consistent language detection
DetectorFactory.seed = 0


def detect_language(text: str) -> str:
    """
    Detect the language of a text.
    Returns a language code (e.g., 'en', 'es').
    Uses only the first 1000 characters for reliability.
    """
    try:
        sample_text = text[:1000]
        lang = detect(sample_text)
        return lang
    except:
        return "unknown"


def translate_text_to_spanish(text: str, max_chunk_size: int = 4500) -> str:
    """
    Translate English text into Spanish, splitting it into chunks
    to avoid API size limits.
    """
    translator = Translator()
    chunks = []
    start = 0

    while start < len(text):
        end = start + max_chunk_size
        if end >= len(text):
            chunks.append(text[start:])
            break

        break_point = text.rfind(' ', start, end)
        if break_point == -1:
            break_point = end
        chunk = text[start:break_point]
        chunks.append(chunk)
        start = break_point + 1

    translated_chunks = []
    for i, chunk in enumerate(chunks):
        try:
            print(f"  Translating chunk {i + 1}/{len(chunks)}... ({len(chunk)} chars)")
            translation = translator.translate(chunk, src='en', dest='es')
            translated_chunks.append(translation.text)
        except Exception as e:
            print(f"    ERROR at chunk {i + 1}: {e}. Using original text for this part.")
            translated_chunks.append(chunk)

    translated_text = " ".join(translated_chunks)
    return translated_text


def process_directory(input_dir: str, output_dir: str):
    """
    Process all .txt files in a folder, detect the language,
    and translate English files into Spanish.
    """
    os.makedirs(output_dir, exist_ok=True)
    translator = Translator()

    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            input_filepath = os.path.join(input_dir, filename)
            output_filepath = os.path.join(output_dir, filename)

            print(f"\nProcessing: {filename}")

            with open(input_filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            if not content.strip():
                print(f"  SKIP: File {filename} is empty.")
                continue

            lang = detect_language(content)
            print(f"  Detected: {lang}")

            if lang == 'en':
                print(f"  Translating EN -> ES...")
                translated_content = translate_text_to_spanish(content)
                with open(output_filepath, 'w', encoding='utf-8') as f:
                    f.write(translated_content)
                print(f"  Saved: {output_filepath} (TRANSLATED)")

            elif lang == 'es':
                print(f"  OK (Spanish). Copying file.")
                with open(output_filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

            else:
                print(f"  WARNING: Unknown language ('{lang}') or detection failed.")
                print(f"  Copying original file without changes.")
                with open(output_filepath, 'w', encoding='utf-8') as f:
                    f.write(content)


# === CONFIGURATION ===
input_directory = "../articles"
output_directory = "../translated_articles"

# === RUN ===
if __name__ == "__main__":
    process_directory(input_directory, output_directory)
    print("\nProcess finished! Check the output folder.")
