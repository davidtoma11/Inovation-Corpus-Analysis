import os
from collections import Counter


def filter_preprocessed_files():
    """
    Post-procesare: elimină DOAR cuvintele cu adevărat problematice
    """
    # LISTĂ OPTIMIZATĂ - elimină doar cuvintele care chiar distorsionează
    words_to_remove = {
        # === NUME PROPII care domină artificial ===
        "aena", "repsol", "indra", "puig", "merlin", "colonial", "acs",
        "santander", "bankinter", "inditex", "arcelormittal", "redeia",
        "accionar", "acciona", "hispasat", "enir", "cnmc", "asg",

        # === TERMENI FINANCIARI GENERICI ===
        "eur", "einf", "ifrs", "isr", "pcaf", "financiero",
        "reaseguro", "asegurador", "actuarial", "prudencial",
        "dudoso", "enajenabl", "subordinado", "reclasificación", "traspaso",

        # === CUVINTE TEHNICE/ADMINISTRATIVE GENERICE ===
        "páginar", "subapartado", "indique", "explique", "incorrección",
        "subsidiario", "planto", "downstream", "sucursal", "concesionario",
        "concesional",

        # === ABREVIERI ȘI ACRONIME ===
        "nfrd", "gar", "icr", "dinf", "pds", "pcaf",

        # === CUVINTE GENERICE FĂRĂ SEMNIFICAȚIE ===
        "ave", "properti", "preocupante", "portafolio", "products", "other",
        "fila", "arabio", "saf", "crudo",

        # === ALTE CUVINTE PROBLEMATICE ===
        "carto", "creador", "relacional", "facilitador", "controlador",
        "memoriar", "memorio", "págín", "vii", "anexos", "vistazo",
        "monto", "gerencia", "var"

        "abreviatura", "insignificante", "oneroso", "ción",
        "emear", "gente", "padre", "coruña",
        "panamá", "dominicano", "peruano", "perú"
    }

    input_folder = "preprocessed_articles"
    output_folder = "preprocessed_articles_filtered"

    os.makedirs(output_folder, exist_ok=True)

    print("🗑️  Removing problematic words from preprocessed files...")

    total_words_removed = 0
    total_original_words = 0

    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Numără cuvintele originale
            words = content.split()
            total_original_words += len(words)

            # Elimină cuvintele nedorite și numără câte au fost eliminate
            filtered_words = []
            words_removed_from_file = 0

            for word in words:
                if word in words_to_remove:
                    words_removed_from_file += 1
                else:
                    filtered_words.append(word)

            total_words_removed += words_removed_from_file
            filtered_content = " ".join(filtered_words)

            # Salvează fișierul filtrat
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(filtered_content)

            print(f"   {filename}: removed {words_removed_from_file} words")

    print(f"\n✅ Filtered files saved to '{output_folder}'")
    print(f"📊 STATISTICS:")
    print(f"   Original words: {total_original_words}")
    print(f"   Words removed: {total_words_removed}")
    print(f"   Remaining words: {total_original_words - total_words_removed}")
    print(f"   Removal percentage: {(total_words_removed / total_original_words) * 100:.1f}%")

    return output_folder


def check_filtered_vocabulary(filtered_folder):
    """
    Verifică noul vocabular după filtrare
    """
    print("\n🔍 Analyzing filtered vocabulary...")

    all_words = []
    for filename in os.listdir(filtered_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(filtered_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                words = content.split()
                all_words.extend(words)

    word_counts = Counter(all_words)
    print(f"📊 Total unique words after filtering: {len(word_counts)}")

    # Afișează cele mai comune cuvinte
    print("\n📈 Top 20 most common words after filtering:")
    print("-" * 40)
    for word, count in word_counts.most_common(20):
        print(f"   {word}: {count}")

    return len(word_counts)


# Rulează post-procesarea
if __name__ == '__main__':
    filtered_folder = filter_preprocessed_files()
    check_filtered_vocabulary(filtered_folder)