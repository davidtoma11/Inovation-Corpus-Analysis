from pathlib import Path
import re


def translate_english_stems_in_files(folder_path):
    """
    Translate English stems into their Spanish equivalents
    inside the preprocessed text files
    """
    folder = Path(folder_path)
    text_files = list(folder.glob("*.txt"))

    # Dictionary for English stem -> Spanish stem
    stem_translation_dict = {
        # Innovation-related stems
        'innov': 'innov',        # stays the same (innovacion → innov)

        # Other common stems
        'technolog': 'tecnolog',
        'develop': 'desarroll',
        'research': 'investig',
        'product': 'product',
        'strateg': 'estrateg',
        'digit': 'digit',
        'busy': 'negoc',         # business → negocio
        'compan': 'empres',      # company → empresa
        'market': 'merc',
        'manag': 'gestion',
        'invest': 'invers',
        'lead': 'lider',
        'growth': 'crecim',
        'custom': 'client',
        'servic': 'servic',
        'business': 'negocio'
    }

    updated_count = 0          # number of files updated
    total_replacements = 0     # total number of stem replacements

    print("Updating English stems inside preprocessed files...")
    print("-" * 60)

    for text_file in text_files:
        try:
            # Read file content
            with open(text_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            original_content = content

            # Replace English stems with Spanish equivalents
            for eng_stem, esp_stem in stem_translation_dict.items():
                if eng_stem in content:
                    # Regex replacement: only full words starting with the stem
                    content = re.sub(r'\b' + eng_stem + r'\w*\b', esp_stem, content)

            # Check if changes were made
            if content != original_content:
                with open(text_file, 'w', encoding='utf-8') as f:
                    f.write(content)

                # Count how many stems were replaced
                changes = sum(1 for eng_stem in stem_translation_dict
                              if eng_stem in original_content and eng_stem not in content)

                total_replacements += changes
                updated_count += 1
                print(f"✓ {text_file.name} - {changes} replacements")
            else:
                print(f"○ {text_file.name} - no changes needed")

        except Exception as e:
            # If something goes wrong, print the error but continue processing
            print(f"✗ Error in {text_file.name}: {str(e)}")

    # Final summary
    print(f"\nProcessing completed!")
    print(f"Files updated: {updated_count}/{len(text_files)}")
    print(f"Total stem replacements: {total_replacements}")


# USAGE
if __name__ == "__main__":
    # Folder with preprocessed text files
    folder_path = "../processed_articles"
    translate_english_stems_in_files(folder_path)
