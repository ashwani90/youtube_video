from openai import OpenAI

OPENAI_API_KEY = "your-openai-api-key"

'''

Twitter Post (Concise, engaging, with hashtags)
🚀 Breaking News! The stock market hits an all-time high! 📈 Experts predict continued growth. Are you ready for the next big opportunity? 💰 #StockMarket #Investing #Finance #BreakingNews

2️⃣ Facebook Post (Detailed, engaging, with emojis)
🔥 BREAKING NEWS! The stock market has soared to an all-time high! 📈💰 Experts predict continued growth, making this a thrilling time for investors. 🚀 Are we heading into a new financial boom? Share your thoughts below! ⬇️👇 #Finance #Investing #StockMarket

3️⃣ LinkedIn Post (Professional, insightful, with a call to action)
📢 Market Update: The stock market has reached an all-time high, and experts forecast continued growth. 📈💡 This is a crucial moment for investors and businesses alike. How are you positioning your portfolio for the next wave of opportunities? Let’s discuss! 👇 #Investing #StockMarket #FinancialGrowth

'''

'''
Here is a good prompt that we can use to generate post
'''

def generate_social_media_posts(script):
    prompt = f"""
    Generate engaging social media posts with max token as 200 based on the following script:

    "Breaking news! The stock market has reached an all-time high. Experts predict continued growth."

    1. **Twitter Post (concise, engaging, with hashtags)**
    2. **Facebook Post (detailed, engaging, with emojis)**
    3. **LinkedIn Post (professional, insightful, with a call to action)**
    """
    
    response = OpenAI(api_key=OPENAI_API_KEY).Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=200
    )

    return response["choices"][0]["text"]

# Example Usage
TEXT_CONTENT = "Breaking news! The stock market has reached an all-time high. Experts predict continued growth."
social_posts = generate_social_media_posts(TEXT_CONTENT)
print("✔ AI-Generated Social Media Posts:\n", social_posts)
