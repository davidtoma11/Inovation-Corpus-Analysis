import pickle
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from collections import Counter
import math


def load_lda_results():
    """Load saved LDA results"""
    with open('lda_results.pkl', 'rb') as f:
        return pickle.load(f)


def create_advanced_visualizations():
    """
    Create advanced visualizations for LDA results
    """
    print("🎨 Creating advanced visualizations...")
    results = load_lda_results()

    # Unpack results
    lda_model = results['lda_model']
    file_names = results['file_names']
    topic_matrix = np.array(results['topic_matrix'])
    topic_distribution = results['topic_distribution']
    num_topics = results['num_topics']

    # Limit to 15 documents for better visualization
    max_docs = min(15, len(file_names))
    file_names = file_names[:max_docs]
    topic_matrix = topic_matrix[:max_docs, :]

    # EXTRACT AND SAVE TOPIC WORDS to simple text file
    print("💬 Extracting and saving topic words...")
    extract_topic_words_simple(lda_model, num_topics)

    # Set style
    plt.style.use('default')
    sns.set_palette("husl")

    # 1. HEATMAP
    print("🔥 Creating enhanced heatmap...")
    create_heatmap(topic_matrix, file_names, num_topics)

    # 2. TOPIC IMPORTANCE CHART
    print("📊 Creating topic importance chart...")
    create_topic_importance_chart(topic_matrix, num_topics)

    # 3. DOCUMENT TOPIC DISTRIBUTION
    print("📈 Creating document distribution chart...")
    create_document_distribution_chart(topic_distribution, num_topics)

    # 4. TOPIC WORD BARCHARTS
    print("📝 Creating topic word barcharts...")
    create_topic_barcharts(lda_model, num_topics)

    # 5. TOPIC CORRELATION HEATMAP
    print("🔗 Creating topic correlation heatmap...")
    create_topic_correlation_heatmap(topic_matrix, num_topics)

    # 6. TOPIC TRENDS
    print("📈 Creating topic trends chart...")
    create_topic_trends_chart(topic_matrix, num_topics)

    # 7. TOPIC WORDS CLOUD
    print("☁️ Creating topic words visualization...")
    create_topic_words_visualization(lda_model, num_topics)

    plt.show()


def extract_topic_words_simple(lda_model, num_topics, topn=15):
    """Extract topic words and save to simple text file"""
    with open('topic_words.txt', 'w', encoding='utf-8') as f:
        f.write("TOPIC WORDS REPORT\n")
        f.write("=" * 50 + "\n\n")

        for topic_idx in range(num_topics):
            words = lda_model.show_topic(topic_idx, topn=topn)
            f.write(f"TOPIC #{topic_idx}:\n")
            f.write("-" * 30 + "\n")
            for i, (word, weight) in enumerate(words, 1):
                f.write(f"{i:2d}. {word:<25} {float(weight):.4f}\n")
            f.write("\n")

    print("💾 Topic words saved to 'topic_words.txt'")


def create_heatmap(topic_matrix, file_names, num_topics):
    """Create enhanced heatmap"""
    fig, ax = plt.subplots(figsize=(14, 10))

    # Create a custom colormap with distinct colors
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
              '#DDA0DD', '#8E44AD', '#3498DB', '#2ECC71', '#E67E22',
              '#F39C12', '#16A085', '#27AE60', '#2980B9', '#9B59B6']
    cmap = LinearSegmentedColormap.from_list('custom_cmap', colors, N=100)

    im = ax.imshow(topic_matrix.T, aspect='auto', cmap=cmap, interpolation='nearest')

    ax.set_yticks(range(num_topics))
    ax.set_yticklabels([f'Topic {i}' for i in range(num_topics)], fontweight='bold')
    ax.set_xticks(range(len(file_names)))
    ax.set_xticklabels([fn[:20] + '...' if len(fn) > 20 else fn for fn in file_names],
                       rotation=45, ha='right', fontsize=9)

    ax.set_xlabel('Documents', fontweight='bold', fontsize=12)
    ax.set_ylabel('Topics', fontweight='bold', fontsize=12)
    ax.set_title('Document-Topic Distribution Heatmap', fontweight='bold', fontsize=14, pad=20)

    cbar = plt.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label('Topic Probability', rotation=270, labelpad=20, fontweight='bold')

    plt.tight_layout()
    plt.savefig('topic_distribution_heatmap.png', dpi=300, bbox_inches='tight')
    print("💾 Heatmap saved")


def create_topic_importance_chart(topic_matrix, num_topics):
    """Create topic importance bar chart"""
    fig, ax = plt.subplots(figsize=(12, 8))
    avg_probs = topic_matrix.mean(axis=0)

    # Create a color for each topic
    colors = plt.cm.tab20(range(num_topics))

    bars = ax.bar(range(num_topics), avg_probs,
                  color=colors, alpha=0.8, edgecolor='black', linewidth=1)

    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height + 0.005,
                f'{height:.3f}', ha='center', va='bottom', fontweight='bold', fontsize=9)

    ax.set_xlabel('Topics', fontweight='bold', fontsize=12)
    ax.set_ylabel('Average Probability', fontweight='bold', fontsize=12)
    ax.set_title('Average Topic Importance Across Documents', fontweight='bold', fontsize=14)
    ax.set_xticks(range(num_topics))
    ax.set_xticklabels([f'Topic {i}' for i in range(num_topics)])
    ax.grid(True, alpha=0.3, axis='y')

    # Add a horizontal line at the average value
    overall_avg = avg_probs.mean()
    ax.axhline(y=overall_avg, color='r', linestyle='--', alpha=0.7, label=f'Overall Average: {overall_avg:.3f}')
    ax.legend()

    plt.tight_layout()
    plt.savefig('topic_importance_chart.png', dpi=300, bbox_inches='tight')
    print("💾 Topic importance chart saved")


def create_document_distribution_chart(topic_distribution, num_topics):
    """Create document distribution pie chart"""
    fig, ax = plt.subplots(figsize=(12, 8))
    topic_counts = Counter([t[1] for t in topic_distribution if t[1] != -1])
    counts = [topic_counts.get(i, 0) for i in range(num_topics)]
    labels = [f'Topic {i}\n({count} docs)' for i, count in enumerate(counts)]

    # Use a colormap with distinct colors
    colors = plt.cm.tab20(range(num_topics))

    wedges, texts, autotexts = ax.pie(counts, labels=labels, autopct='%1.1f%%',
                                      startangle=90, colors=colors)

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(9)

    ax.set_title('Document Distribution Across Topics', fontweight='bold', fontsize=14)
    plt.tight_layout()
    plt.savefig('topic_distribution_pie.png', dpi=300, bbox_inches='tight')
    print("💾 Distribution pie chart saved")


def create_topic_barcharts(lda_model, num_topics):
    """Create bar charts for topic words"""
    cols = min(4, num_topics)  # maximum number of columns
    rows = math.ceil(num_topics / cols)

    fig, axes = plt.subplots(rows, cols, figsize=(cols * 5, rows * 4))
    axes = axes.flatten()

    for topic_idx in range(num_topics):
        topic_words = lda_model.show_topic(topic_idx, topn=8)  # Show only top 8 words
        words = [word for word, weight in topic_words]
        weights = [weight for word, weight in topic_words]

        y_pos = np.arange(len(words))
        bars = axes[topic_idx].barh(y_pos, weights, color=plt.cm.tab20(topic_idx), alpha=0.8)

        axes[topic_idx].set_yticks(y_pos)
        axes[topic_idx].set_yticklabels(words, fontsize=10)
        axes[topic_idx].set_xlabel('Weight', fontsize=10)
        axes[topic_idx].set_title(f'Topic {topic_idx} - Top Words', fontweight='bold', fontsize=12)
        axes[topic_idx].grid(True, alpha=0.3, axis='x')
        axes[topic_idx].set_xlim(0, max(weights) * 1.1)

        for i, bar in enumerate(bars):
            width = bar.get_width()
            axes[topic_idx].text(width + 0.001, bar.get_y() + bar.get_height() / 2.,
                                 f'{width:.3f}', ha='left', va='center', fontsize=9)

    # remove empty subplots if any
    for j in range(num_topics, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.savefig('topic_word_barcharts.png', dpi=300, bbox_inches='tight')
    print("💾 Topic word barcharts saved")


def create_topic_correlation_heatmap(topic_matrix, num_topics):
    """Create topic correlation heatmap"""
    fig, ax = plt.subplots(figsize=(10, 8))
    correlation_matrix = np.corrcoef(topic_matrix.T)

    im = ax.imshow(correlation_matrix, cmap='RdBu_r', vmin=-1, vmax=1, aspect='equal')

    # Add correlation values to cells
    for i in range(num_topics):
        for j in range(num_topics):
            color = 'white' if abs(correlation_matrix[i, j]) > 0.5 else 'black'
            ax.text(j, i, f'{correlation_matrix[i, j]:.2f}',
                    ha='center', va='center', fontweight='bold',
                    color=color, fontsize=8)

    ax.set_xticks(range(num_topics))
    ax.set_yticks(range(num_topics))
    ax.set_xticklabels([f'T{i}' for i in range(num_topics)])
    ax.set_yticklabels([f'T{i}' for i in range(num_topics)])
    ax.set_title('Topic Correlation Matrix', fontweight='bold', fontsize=14)

    cbar = plt.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label('Correlation Coefficient', rotation=270, labelpad=20)

    plt.tight_layout()
    plt.savefig('topic_correlation_heatmap.png', dpi=300, bbox_inches='tight')
    print("💾 Correlation heatmap saved")


def create_topic_trends_chart(topic_matrix, num_topics):
    """Create topic trends across documents"""
    fig, ax = plt.subplots(figsize=(14, 8))

    # Use a colormap with distinct colors
    colors = plt.cm.tab20(range(num_topics))

    for topic_idx in range(num_topics):
        ax.plot(topic_matrix[:, topic_idx],
                label=f'Topic {topic_idx}',
                linewidth=2,
                marker='o',
                markersize=4,
                color=colors[topic_idx])

    ax.set_xlabel('Document Index', fontweight='bold', fontsize=12)
    ax.set_ylabel('Topic Probability', fontweight='bold', fontsize=12)
    ax.set_title('Topic Probability Trends Across Documents', fontweight='bold', fontsize=14)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
    ax.grid(True, alpha=0.3)

    # Set x-axis to show document indices
    ax.set_xticks(range(len(topic_matrix)))

    plt.tight_layout()
    plt.savefig('topic_trends_chart.png', dpi=300, bbox_inches='tight')
    print("💾 Topic trends chart saved")


def create_topic_words_visualization(lda_model, num_topics):
    """Create a visualization of top words for each topic"""
    fig, axes = plt.subplots(num_topics, 1, figsize=(10, 3 * num_topics))

    if num_topics == 1:
        axes = [axes]

    for topic_idx in range(num_topics):
        topic_words = lda_model.show_topic(topic_idx, topn=6)  # Show only top 6 words
        words = [word for word, weight in topic_words]
        weights = [weight for word, weight in topic_words]

        # Create horizontal bar chart
        y_pos = np.arange(len(words))
        axes[topic_idx].barh(y_pos, weights, color=plt.cm.tab20(topic_idx), alpha=0.8)
        axes[topic_idx].set_yticks(y_pos)
        axes[topic_idx].set_yticklabels(words, fontsize=11)
        axes[topic_idx].set_xlabel('Weight', fontsize=10)
        axes[topic_idx].set_title(f'Topic {topic_idx} - Key Words', fontweight='bold', fontsize=12)
        axes[topic_idx].grid(True, alpha=0.3, axis='x')

        # Add value labels to bars
        for i, v in enumerate(weights):
            axes[topic_idx].text(v + 0.01, i, f'{v:.3f}', va='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig('topic_words_visualization.png', dpi=300, bbox_inches='tight')
    print("💾 Topic words visualization saved")


if __name__ == '__main__':
    create_advanced_visualizations()