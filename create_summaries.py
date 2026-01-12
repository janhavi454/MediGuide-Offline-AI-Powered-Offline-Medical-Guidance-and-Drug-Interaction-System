
"""
Simple script to create summaries from existing medical articles
"""
import json
import os
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def summarize_text(text, max_length=200):
    """Generate a summary of the text using extractive summarization"""
    if len(text) <= max_length:
        return text

    # Simple extractive summarization
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    if len(sentences) <= 3:
        return text[:max_length] + "..."

    # Take first and last sentences, and middle if available
    summary_sentences = []
    summary_sentences.append(sentences[0])  # First sentence

    if len(sentences) > 2:
        summary_sentences.append(sentences[len(sentences)//2])  # Middle sentence

    if len(sentences) > 1:
        summary_sentences.append(sentences[-1])  # Last sentence

    summary = '. '.join(summary_sentences)
    if len(summary) > max_length:
        summary = summary[:max_length-3] + "..."

    return summary

def create_summaries_from_articles():
    """Create summaries from existing medical articles"""
    articles_file = "app/data/medical_wikipedia_data/medical_articles.json"
    summaries_file = "app/data/medical_wikipedia_data/medical_summaries.json"

    if not os.path.exists(articles_file):
        print(f"Articles file not found: {articles_file}")
        return

    print("Loading medical articles...")
    with open(articles_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    print(f"Found {len(articles)} articles. Creating summaries...")

    summaries = []
    for i, article in enumerate(articles):
        if i % 100 == 0:
            print(f"Processed {i}/{len(articles)} articles...")

        # Generate summary
        summary_text = summarize_text(article['content'], max_length=200)

        summary_data = {
            "id": article['id'],
            "title": article['title'],
            "url": article['url'],
            "summary": summary_text,
            "summary_length": len(summary_text),
            "original_length": article['length'],
            "source": "wikipedia_medical_mini"
        }
        summaries.append(summary_data)

    print(f"Saving {len(summaries)} summaries to {summaries_file}...")
    with open(summaries_file, 'w', encoding='utf-8') as f:
        json.dump(summaries, f, indent=2, ensure_ascii=False)

    print("Summary creation complete!")
    return summaries

if __name__ == "__main__":
    create_summaries_from_articles()
