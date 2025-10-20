# Methodology for Innovation Analysis

## 1. Purpose of the Study
The purpose of this study is to analyze how the concept of **“innovation”** is perceived, discussed, and integrated within a set of 50 working documents from various companies.  

Using **Natural Language Processing (NLP)** techniques—particularly *topic modeling*—the study aims to uncover semantic patterns, thematic clusters, and contextual uses of innovation-related terms across multilingual corporate documents.

## 2. Data Collection and Preparation (Corpus)
- A dataset of **50 internal company documents** was collected, written in both English and Spanish.  
- Each document was converted from **PDF to plain text** format using automated text extraction tools.  
- To ensure traceability and facilitate error detection, each PDF was saved as a separate **.txt file**.  
- All texts were then aggregated into a **Python list of document strings**, forming the analysis corpus.  
- Each document was treated as an **independent analytical unit** for subsequent preprocessing and topic modeling.

## 3. Text Preprocessing / Postprocessing
To ensure linguistic uniformity and data quality, the following steps were applied:

1. **Translation**  
   - All documents were automatically translated into **Spanish** using reliable machine translation tools.  
   - This step ensured consistent topic modeling on a *single-language corpus*.

2. **Tokenization**  
   - Texts were split into individual tokens (words), removing punctuation and special characters.

3. **Stop Word Removal**  
   - A Spanish stop word list was applied to remove common, semantically weak words (e.g., *y, pero, que, de, el*).

4. **Lemmatization / Stemming**  
   - Tokens were reduced to their **root forms**, allowing morphological variants to be treated as one.  
   - Example: *innovación, innovar, innovador, innovativa → innova*.

5. **Filtering**  
   - Extremely rare words (appearing in fewer than 2 documents) and overly frequent words (present in more than 80% of the corpus) were excluded.

6. **Postprocessing**  
   - Cleaned and lemmatized tokens were further refined by removing **non-informative words**, retaining only *semantically relevant tokens* for modeling.

## 4. Topic Modeling Implementation
- **Algorithm Used:** Latent Dirichlet Allocation (**LDA**) implemented with **Gensim (Python)**.

- **Parameters:**  
  - Number of topics: **6** (chosen empirically based on coherence score)  
  - Hyperparameters `alpha` and `eta`: set to *auto* for adaptive optimization  
  - Training: 50 passes with a fixed random state for reproducibility

- **Corpus Representation:**  
  - Each document tokenized and converted into a **bag-of-words vector**  
  - Rare (<2 documents) and overly frequent (>80% corpus) words were filtered out

- **Model Output:**  
  - Topics with **representative keywords and weights**  
  - Document-topic distributions and **dominant topic** per document  
  - **Coherence score** for evaluating topic quality

## 5. Analysis and Interpretation of Results
- **Topic Review:** Top keywords for each topic were examined for thematic coherence.  
- **Innovation-Focused Topics:** Topics containing the root *innova* among the top 15–20 words were selected.  
- **Semantic Interpretation:** Qualitative analysis was conducted to understand how innovation is contextualized.  
- **Visualization:** Results were visualized with **bar charts, topic maps, and co-occurrence graphs** to highlight relationships between topics.



## Drive link (for documents and illustrations):
https://drive.google.com/drive/folders/1WvSF0oitDlccMd22maO1BMcIjK-qkToZ?usp=drive_link
