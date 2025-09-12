import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer, SnowballStemmer
import re
from pathlib import Path
from collections import Counter

# Download all necessary NLTK resources
try:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('punkt_tab')  # Extra resource sometimes required
    print("All NLTK resources are installed correctly.")
except:
    print("Error downloading NLTK resources. Please check your internet connection.")


class TextPreprocessor:
    def __init__(self):
        # Initialize text preprocessor with both English and Spanish settings
        try:
            # Load stopwords (words without much meaning)
            self.stopwords_en = set(stopwords.words('english'))   # English stopwords
            self.stopwords_es = set(stopwords.words('spanish'))   # Spanish stopwords
        except:
            # If NLTK stopwords are missing, keep empty sets to avoid crashes
            print("Error loading stopwords. Please check NLTK installation.")
            self.stopwords_en = set()
            self.stopwords_es = set()

        # Tools for reducing words to their base form
        self.lemmatizer_en = WordNetLemmatizer()       # For English (lemmatization)
        self.stemmer_es = SnowballStemmer('spanish')   # For Spanish (stemming)

        # Custom stopwords (manually added useless words)
        self.custom_stopwords = {
            'page', 'section', 'chapter', 'figure', 'table',
            'http', 'https', 'www', 'com', 'org', 'pdf',
            'nbsp', 'ie', 'eg', 'etc', 'viz'
        }

        # Merge built-in stopwords with custom ones
        self.stopwords_en.update(self.custom_stopwords)
        self.stopwords_es.update(self.custom_stopwords)

    def detect_language(self, text):
        # Detect language based on presence of common words
        if not text.strip():
            return 'english'  # Default if the text is empty

        # Common words in Spanish
        spanish_words = {'el', 'la', 'los', 'las', 'de', 'que', 'y', 'en', 'un', 'una', 'es', 'por', 'con'}
        # Common words in English
        english_words = {'the', 'and', 'of', 'to', 'in', 'a', 'is', 'that', 'for', 'on', 'with', 'by', 'as'}

        text_lower = text.lower()
        es_count = sum(1 for word in spanish_words if word in text_lower)
        en_count = sum(1 for word in english_words if word in text_lower)

        # Choose the language with more matches
        return 'spanish' if es_count > en_count else 'english'

    def clean_text(self, text):
        # Clean raw text (remove noise and normalize)
        if not text:
            return ""

        # Remove page headers (if still present)
        text = re.sub(r'--- Page \d+ ---', '', text)

        # Remove numbers
        text = re.sub(r'\d+', '', text)

        # Remove punctuation and special symbols
        text = re.sub(r'[^\w\s]', ' ', text)

        # Convert to lowercase
        text = text.lower()

        # Replace multiple spaces with a single one
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def simple_tokenize(self, text):
        # Simple tokenization without NLTK (fallback method)
        tokens = re.findall(r'\b[a-zA-Z]+\b', text)
        return tokens

    def tokenize_and_filter(self, text, language):
        # Tokenize text and remove stopwords / useless tokens
        if not text.strip():
            return []

        try:
            # Try tokenization with NLTK
            tokens = word_tokenize(text)
        except:
            # Fallback to simple regex-based tokenizer
            tokens = self.simple_tokenize(text)

        filtered_tokens = []
        for token in tokens:
            # Keep only words that:
            # - are longer than 2 characters
            # - are not stopwords
            # - contain only letters
            if (len(token) > 2 and
                    token not in self.stopwords_en and
                    token not in self.stopwords_es and
                    token.isalpha()):
                filtered_tokens.append(token)

        return filtered_tokens

    def lemmatize_tokens(self, tokens, language):
        # Reduce words to their base form (depends on language)
        processed_tokens = []

        if language == 'english':
            # For English: lemmatization (more accurate)
            for token in tokens:
                lemma = self.lemmatizer_en.lemmatize(token)
                processed_tokens.append(lemma)
        else:
            # For Spanish: stemming (faster, but less precise)
            for token in tokens:
                stem = self.stemmer_es.stem(token)
                processed_tokens.append(stem)

        return processed_tokens

    def preprocess_document(self, text):
        # Run full preprocessing pipeline on a single document
        if not text or not text.strip():
            return [], 'english'

        # Step 1: Detect language
        language = self.detect_language(text)

        # Step 2: Clean raw text
        cleaned_text = self.clean_text(text)

        # Step 3: Tokenize and filter
        tokens = self.tokenize_and_filter(cleaned_text, language)

        # Step 4: Lemmatize or stem tokens
        processed_tokens = self.lemmatize_tokens(tokens, language)

        return processed_tokens, language

    def preprocess_folder(self, input_folder, output_folder):
        # Preprocess all text files in a folder
        input_path = Path(input_folder)
        output_path = Path(output_folder)
        output_path.mkdir(exist_ok=True)

        text_files = list(input_path.glob("*.txt"))

        if not text_files:
            print("No text files found in the folder.")
            return [], Counter()

        print(f"Processing {len(text_files)} text files...")
        print("-" * 50)

        all_processed_docs = []
        language_stats = Counter()

        for i, text_file in enumerate(text_files, 1):
            try:
                # Read the raw text file
                with open(text_file, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()

                if not text.strip():
                    # Skip empty files
                    print(f"[{i}/{len(text_files)}] {text_file.name} - SKIP (empty file)")
                    continue

                # Run full preprocessing
                processed_tokens, language = self.preprocess_document(text)

                # Save the processed output
                output_file = output_path / f"processed_{text_file.name}"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(' '.join(processed_tokens))

                # Collect statistics
                language_stats[language] += 1
                all_processed_docs.append(processed_tokens)

                print(f"[{i}/{len(text_files)}] {text_file.name} "
                      f"({language}, {len(processed_tokens)} tokens)")

            except Exception as e:
                print(f"Error processing {text_file.name}: {str(e)}")

        # Print summary
        print("\n" + "=" * 50)
        print("PREPROCESSING SUMMARY")
        print("=" * 50)
        print(f"Files processed: {len(text_files)}")
        print(f"Language distribution: {dict(language_stats)}")

        return all_processed_docs, language_stats


# MAIN PROGRAM - Run preprocessing on the "articles" folder
if __name__ == "__main__":
    # Initialize preprocessor
    preprocessor = TextPreprocessor()

    # Input (raw articles) and output (cleaned articles) folders
    input_folder = "articles"
    output_folder = "processed_articles"

    # Process all text files
    processed_docs, language_stats = preprocessor.preprocess_folder(input_folder, output_folder)

    # Extra analysis on processed docs
    if processed_docs:
        # Check how many docs mention "innovation" terms
        innovation_terms = {'innova', 'innov', 'innovation', 'innovacion'}
        innovation_count = 0

        for doc in processed_docs:
            if any(term in ' '.join(doc) for term in innovation_terms):
                innovation_count += 1

        print(f"\nDocuments mentioning innovation: {innovation_count}/{len(processed_docs)}")

        # Vocabulary analysis
        all_tokens = [token for doc in processed_docs for token in doc]
        vocab = Counter(all_tokens)

        print(f"\nVocabulary analysis:")
        print(f"Total tokens: {len(all_tokens)}")
        print(f"Unique tokens: {len(vocab)}")
        print(f"Top 10 most common words:")

        for word, count in vocab.most_common(10):
            print(f"  {word}: {count}")

        print(f"\nAll done! Preprocessed files saved in '{output_folder}'")
    else:
        print("No files were processed.")
