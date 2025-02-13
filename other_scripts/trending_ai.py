import json

'''
Simply get trending news
May also be needed for future to add more links
'''

def get_trending_news():
    API_URL = "https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=your-newsapi-key"
    response = requests.get(API_URL)
    news_data = response.json()

    if news_data["status"] == "ok":
        articles = news_data["articles"][:3]  # Get top 3 headlines
        news_script = "\n".join([f"{i+1}. {article['title']}" for i, article in enumerate(articles)])
        return f"Today's trending news:\n{news_script}"
    else:
        return "No news found."

# Fetch trending news and use it in our video
TEXT_CONTENT = get_trending_news()
print("✔ AI-Generated Script:\n", TEXT_CONTENT)
