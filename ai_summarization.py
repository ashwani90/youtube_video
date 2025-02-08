import requests
from transformers import pipeline

def extract_text_from_html(text):
    return text

def summarize_article(url):
    response = requests.get(url)
    article_text = extract_text_from_html(response.text)  # Extract article text (implement this function)
    
    summarizer = pipeline("summarization")
    summary = summarizer(article_text, max_length=150, min_length=50, do_sample=False)[0]["summary_text"]
    
    return summary

# Example Usage
article_url = "https://example.com/news-article"
TEXT_CONTENT = summarize_article(article_url)
print("✔ AI-Generated Summary:", TEXT_CONTENT)
