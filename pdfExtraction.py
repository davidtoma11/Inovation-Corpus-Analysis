import fitz
from pathlib import Path
import time


def extract_pdf_text(pdf_file, output_folder):
    # Extract text from one PDF and save it as a .txt file
    # Returns number of pages processed (0 if fails)
    output_path = Path(output_folder)
    output_file = output_path / f"{pdf_file.stem}.txt"

    try:
        with fitz.open(pdf_file) as doc:
            total_pages = len(doc)

            with open(output_file, 'w', encoding='utf-8') as f:
                for page_num in range(total_pages):
                    page = doc[page_num]
                    text = page.get_text()

                    # Write page text with page marker (helps human verification)
                    f.write(f"--- Page {page_num + 1} ---\n")
                    f.write(text + "\n\n")

            return total_pages

    except Exception as e:
        print(f"Error processing {pdf_file.name}: {str(e)}")
        return 0


def process_pdf_folder(input_folder, output_folder):
    # Process all PDFs from input folder and save extracted text in output folder
    # Recomandation: good to double-check (human verify) output files, some PDFs / pages may fail extraction
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    output_path.mkdir(exist_ok=True)

    # Collect all PDF files
    pdf_files = list(input_path.glob("*.pdf"))
    total_files = len(pdf_files)

    if total_files == 0:
        print("No PDF files found in the input folder.")
        return

    print(f"Found {total_files} PDF files to process...")
    print("-" * 50)

    success_count = 0
    total_pages_processed = 0

    # Iterate through each PDF file
    for i, pdf_file in enumerate(pdf_files, 1):
        start_time = time.time()

        # Extract text for current file
        page_count = extract_pdf_text(pdf_file, output_folder)

        if page_count > 0:
            success_count += 1
            total_pages_processed += page_count
            processing_time = time.time() - start_time

            # Show success message with details
            print(f"[{i}/{total_files}] Processed: {pdf_file.name} ({page_count} pages, {processing_time:.1f}s)")
        else:
            print(f"[{i}/{total_files}] Failed: {pdf_file.name}")

    # Print summary at the end
    print("=" * 50)
    print("PROCESSING SUMMARY")
    print("=" * 50)
    print(f"Total files: {total_files}")
    print(f"Successfully processed: {success_count}")
    print(f"Total pages extracted: {total_pages_processed}")

    if success_count < total_files:
        print(f"Failed to process: {total_files - success_count} files")


if __name__ == "__main__":
    # Define input (where PDFs are) and output (where .txt files go)
    input_folder = r"C:\Users\Lenovo\OneDrive\Desktop\Paper informe_innov"
    output_folder = "articles"

    process_pdf_folder(input_folder, output_folder)
