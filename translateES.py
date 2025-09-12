from pathlib import Path
import re


def translate_english_stems_in_files(folder_path):
    """
    Traduce rădăcinile englezești din fișierele preprocesate
    """
    folder = Path(folder_path)
    text_files = list(folder.glob("*.txt"))

    # Dicționar pentru rădăcini englezești -> spaniole
    stem_translation_dict = {
        # Rădăcini de inovație
        'innov': 'innov',  # Rămâne la fel (innovacion → innov)

        # Alte rădăcini comune
        'technolog': 'tecnolog',
        'develop': 'desarroll',
        'research': 'investig',
        'product': 'product',
        'strateg': 'estrateg',
        'digit': 'digit',
        'busy': 'negoc',  # business → negocio
        'compan': 'empres',  # company → empresa
        'market': 'merc',
        'manag': 'gestion',
        'invest': 'invers',
        'lead': 'lider',
        'growth': 'crecim',
        'custom': 'client',
        'servic': 'servic',
        'business': 'negocio'
    }

    updated_count = 0
    total_replacements = 0

    print("Actualizez rădăcini englezești în fișierele preprocesate...")
    print("-" * 60)

    for text_file in text_files:
        try:
            with open(text_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            original_content = content

            # Înlocuiește rădăcinile englezești
            for eng_stem, esp_stem in stem_translation_dict.items():
                # Înlocuiește doar dacă rădăcina există
                if eng_stem in content:
                    # Folosește regex pentru a înlocui doar cuvintele întregi care încep cu rădăcina
                    content = re.sub(r'\b' + eng_stem + r'\w*\b', esp_stem, content)

            # Verifică dacă s-au făcut modificări
            if content != original_content:
                with open(text_file, 'w', encoding='utf-8') as f:
                    f.write(content)

                # Numără câte înlocuiri s-au făcut
                changes = sum(1 for eng_stem in stem_translation_dict
                              if eng_stem in original_content and eng_stem not in content)

                total_replacements += changes
                updated_count += 1
                print(f"✓ {text_file.name} - {changes} înlocuiri")
            else:
                print(f"○ {text_file.name} - nicio modificare necesară")

        except Exception as e:
            print(f"✗ Eroare la {text_file.name}: {str(e)}")

    print(f"\nProcesare completă!")
    print(f"Fișiere actualizate: {updated_count}/{len(text_files)}")
    print(f"Total înlocuiri de rădăcini: {total_replacements}")


# Utilizare
if __name__ == "__main__":
    folder_path = "processed_articles"  # Folderul cu fișierele preprocesate
    translate_english_stems_in_files(folder_path)