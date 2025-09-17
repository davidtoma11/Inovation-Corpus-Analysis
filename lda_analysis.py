import os
import gensim
import gensim.corpora as corpora
from gensim.models import CoherenceModel
from collections import Counter
import pickle


def run_lda_analysis():
    # Run LDA analysis and save results for visualization
    print("Loading preprocessed documents...")
    documents = []
    file_names = []
    preprocessed_folder = "preprocessed_articles"

    for filename in os.listdir(preprocessed_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(preprocessed_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                tokens = content.split()
                if tokens:
                    documents.append(tokens)
                    file_names.append(filename)

    print(f"Loaded {len(documents)} documents.")

    # Create dictionary and corpus
    print("🔨 Creating dictionary and corpus...")
    id2word = corpora.Dictionary(documents)
    id2word.filter_extremes(no_below=5, no_above=0.4)
    corpus = [id2word.doc2bow(text) for text in documents]

    print(f"Dictionary: {len(id2word)} unique words")
    print(f"Corpus: {len(corpus)} documents")

    # Train LDA model
    num_topics = 6
    print(f"Training LDA model with {num_topics} topics...")

    lda_model = gensim.models.ldamodel.LdaModel(
        corpus=corpus,
        id2word=id2word,
        num_topics=num_topics,
        random_state=100,
        passes=50,
        alpha='auto',
        eta='auto',
        per_word_topics=True
    )

    # Compute coherence
    print("Computing coherence score...")
    coherence_model = CoherenceModel(
        model=lda_model,
        texts=documents,
        dictionary=id2word,
        coherence='c_v',
        processes=1
    )
    coherence_score = coherence_model.get_coherence()
    print(f'Coherence Score: {coherence_score:.4f}')

    # Get document-topic distributions
    print("Calculating document-topic distributions...")
    topic_matrix = []
    for doc_bow in corpus:
        topic_dist = lda_model.get_document_topics(doc_bow, minimum_probability=0)
        topic_probs = [prob for _, prob in topic_dist]
        topic_matrix.append(topic_probs)

    # Get dominant topics
    topic_distribution = []
    for i, doc_bow in enumerate(corpus):
        topic_probs = lda_model.get_document_topics(doc_bow)
        if topic_probs:
            dominant_topic = max(topic_probs, key=lambda x: x[1])[0]
            topic_distribution.append((i, dominant_topic, file_names[i]))
        else:
            topic_distribution.append((i, -1, file_names[i]))

    # Save results for visualization
    results = {
        'lda_model': lda_model,
        'id2word': id2word,
        'corpus': corpus,
        'documents': documents,
        'file_names': file_names,
        'topic_matrix': topic_matrix,
        'topic_distribution': topic_distribution,
        'coherence_score': coherence_score,
        'num_topics': num_topics
    }

    with open('lda_results.pkl', 'wb') as f:
        pickle.dump(results, f)

    print("Results saved to 'lda_results.pkl'")

    # Show summary
    print("\n" + "=" * 60)
    print("LDA ANALYSIS SUMMARY")
    print("=" * 60)

    topic_counts = Counter([t[1] for t in topic_distribution])
    for topic_id, count in topic_counts.most_common():
        if topic_id != -1:
            print(f"Topic #{topic_id}: {count} documents")

    return results


if __name__ == '__main__':
    run_lda_analysis()