import spacy
import re
import os
from spacy.lang.es.stop_words import STOP_WORDS as ES_STOP_WORDS

# === CONFIGURATION ===
INPUT_DIR = "translated_articles"
OUTPUT_DIR = "preprocessed_articles"

# Custom stopwords and ignored terms
custom_stopwords = {
    "información", "dato", "documento", "pdf", "página", "año", "años", "empresa", "empresas",
    "través", "vez", "ser", "según", "respecto", "número", "ciento", "podría", "ley", "artículo",
    "punto", "parte", "tal", "decreto", "fin", "tipo", "nombre", "etc", "etcétera", "cómo", "cual",
    "cuales", "donde", "mismo", "tan", "así", "si", "sí", "sino", "sólo", "solamente", "hacer", "tener",
    "debe", "debería", "deberá", "poder", "puede", "pueden", "gran", "mayor", "menor", "nuevo", "nueva",
    "buen", "buena", "importante", "diferente", "respectivo", "principal", "general", "específico",
    "actual", "cierto", "varios", "varias", "otros", "otras", "cada", "todo", "toda", "todos", "todas",
    "solo", "sola", "solos", "solas", "sino", "ambos", "ambas", "ninguno", "ninguna", "alguno", "alguna",
    "algo", "sido", "estado", "ser", "estar", "haber", "hacer", "tener", "decir", "ver", "ir", "dar",
    "saber", "querer", "llegar", "pasar", "deber", "poner", "parecer", "quedar", "creer", "hablar",
    "llevar", "dejar", "seguir", "encontrar", "llamar", "venir", "pensar", "salir", "volver", "tomar",
    "conseguir", "tratar", "mirar", "empezar", "esperar", "buscar", "existir", "entrar", "trabajar",
    "escribir", "permitir", "aparecer", "conocer", "realizar", "comenzar", "considerar", "perder",
    "producir", "presentar", "mantener", "significar", "cambiar", "señalar", "suponer", "lograr",
    "incluir", "explicar", "entender", "desarrollar", "recordar", "utilizar", "mostrar", "indicar",
    "evaluar", "analizar", "definir", "establecer", "identificar", "reconocer", "determinar",
    "constituir", "generar", "manifestar", "obtener", "ofrecer", "pertenecer", "proporcionar",
    "representar", "surgir", "utilizar", "valorar", "aportar", "comprender", "configurar", "constatar",
    "contar", "contribuir", "controlar", "demostrar", "diseñar", "ejecutar", "elegir", "elevar",
    "emplear", "encargar", "enfocar", "ensayar", "estudiar", "evitar", "exigir", "expresar", "formar",
    "implicar", "impulsar", "integrar", "intentar", "invertir", "lograr", "mostrar", "motivar", "notar",
    "objetivar", "observar", "obtener", "organizar", "orientar", "participar", "planificar", "precisar",
    "preparar", "pretender", "probar", "proceder", "procurar", "promover", "proponer", "proteger",
    "proveer", "publicar", "recibir", "reclamar", "reconocer", "referir", "reflejar", "registrar",
    "regular", "relacionar", "remitir", "repetir", "reportar", "requerir", "resolver", "responder",
    "resultar", "reunir", "revisar", "solicitar", "subir", "sugerir", "superar", "temer", "terminar",
    "testar", "tocar", "transformar", "transmitir", "usar", "valer", "variar", "visualizar", "vivir"
}
ALL_STOPWORDS = ES_STOP_WORDS.union(custom_stopwords)

# Load spaCy model
print("Loading spaCy model...")
nlp = spacy.load("es_core_news_sm", disable=['parser', 'ner'])
print("Model loaded!")


def process_large_text(text, chunk_size=1000000):
    """
    Process very large texts by splitting them into smaller chunks.
    """
    all_processed_tokens = []
    for start in range(0, len(text), chunk_size):
        end = start + chunk_size
        chunk = text[start:end]

        if end < len(text):
            last_space = chunk.rfind(' ')
            if last_space != -1:
                end = start + last_space
                chunk = text[start:end]

        processed_chunk = process_text_chunk(chunk)
        all_processed_tokens.extend(processed_chunk)

    return all_processed_tokens


def process_text_chunk(text):
    """
    Process a text chunk with aggressive preprocessing.
    """
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()

    if not text:
        return []

    doc = nlp(text)
    processed_tokens = []

    for token in doc:
        if token.pos_ in {'NOUN', 'VERB', 'ADJ', 'ADV'}:
            if token.lemma_ not in ALL_STOPWORDS:
                if 2 < len(token.lemma_) < 25:
                    processed_tokens.append(token.lemma_)

    return processed_tokens


def process_all_files(input_dir, output_dir):
    """
    Process all .txt files from the input directory
    and save preprocessed results into the output directory.
    """
    os.makedirs(output_dir, exist_ok=True)
    all_files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]
    total_files = len(all_files)

    print(f"Starting preprocessing of {total_files} files...")

    for i, filename in enumerate(all_files, 1):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        print(f"[{i}/{total_files}] Processing: {filename}")

        try:
            with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"    ERROR reading {filename}: {e}")
            continue

        file_size = len(content)
        print(f"    Size: {file_size} characters")

        try:
            if file_size > 500000:
                print(f"    Large file - processing in chunks...")
                preprocessed_tokens = process_large_text(content)
            else:
                preprocessed_tokens = process_text_chunk(content)

            print(f"    Extracted tokens: {len(preprocessed_tokens)}")

        except Exception as e:
            print(f"    ERROR preprocessing {filename}: {e}")
            continue

        output_content = " ".join(preprocessed_tokens)

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(output_content)
        except Exception as e:
            print(f"    ERROR writing {filename}: {e}")
            continue

    print("Preprocessing completed!")


# === RUN ===
if __name__ == "__main__":
    process_all_files(INPUT_DIR, OUTPUT_DIR)
