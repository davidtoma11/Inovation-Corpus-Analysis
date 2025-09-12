from pathlib import Path
import re


def remove_page_headers_from_folder(folder_path):
    # Remove all "--- Page X ---" headers from text files in a folder
    # Also print how many headers were removed for each file
    folder = Path(folder_path)
    text_files = list(folder.glob("*.txt"))

    if not text_files:
        print("No text files found in the folder.")
        return

    print(f"Found {len(text_files)} text files to clean...")
    print("-" * 50)

    total_headers_removed = 0
    files_processed = 0

    # Go through each .txt file
    for text_file in text_files:
        try:
            with open(text_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Count headers before cleaning
            headers_before = content.count('--- Page ')

            # Remove all headers with regex
            cleaned_content = re.sub(r'--- Page \d+ ---\n', '', content)

            # Write cleaned text back to the same file
            with open(text_file, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)

            # Count how many headers were removed
            headers_after = cleaned_content.count('--- Page ')
            headers_removed = headers_before - headers_after

            total_headers_removed += headers_removed
            files_processed += 1

            print(f"Cleaned: {text_file.name} - Removed {headers_removed} page headers")

        except Exception as e:
            print(f"Error cleaning {text_file.name}: {str(e)}")

    # Print summary at the end
    print("=" * 50)
    print("CLEANING SUMMARY")
    print("=" * 50)
    print(f"Files processed: {files_processed}")
    print(f"Total headers removed: {total_headers_removed}")


# Example usage
folder_path = "../articles"  # Path to folder with text files
remove_page_headers_from_folder(folder_path)
