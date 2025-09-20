# Methodology for Innovation Analysis

### 1. Purpose of the study
The goal of this study is to see how the concept of "innovation" is understood and used in 50 working documents from different companies. The analysis uses Natural Language Processing (NLP) techniques, with a focus on topic modeling.


### 2. Data collection and preparation (Corpus)
- We have collected a dataset of 50 documents, written in both English and Spanish.
-	The text from each PDF document was extracted and stored in a single data structure (a list of strings).


### 3. Text preprocessing
Before applying the algorithm, the texts went through a cleaning process to ensure better data quality:
- Tokenization: Each document was split into individual words (tokens).
-	Stop word removal: Very common words with little meaning (like "and", "but", "el") were removed using language-specific stop word lists for English and Spanish.
-	Lemmatization/Stemming: Words were reduced to their base/root form. For example: innovation, innovating, innovate, innovative and innovacion - all reduced to innova.
-	Filtering: Words that were too rare or too frequent were removed, since they don’t help with topic analysis.


### 4. Topic modeling implementation
-	Algorithm used: Latent Dirichlet Allocation (LDA) from Python’s Gensim library.


### 5. Analysis and interpretation of results
-	Topic analysis: The keywords for each topic identified by the algorithm were reviewed.
-	Innovation-related topics: The topics containing the root innova among the top 10 words were selected.
-	Semantic interpretation: A qualitative analysis was done on the other words in these topics to see how innovation is contextualized (e.g., product innovation, process innovation, organizational innovation).
-	Visualization: Results will be presented using charts (bar graphs, topic maps, etc.) to make the relationships between topics easier to understand.


## Drive link (for documents and illustrations):
https://drive.google.com/drive/folders/1WvSF0oitDlccMd22maO1BMcIjK-qkToZ?usp=drive_link
