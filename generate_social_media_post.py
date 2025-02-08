from openai import OpenAI

OPENAI_API_KEY = "your-openai-api-key"

def generate_social_media_posts(script):
    prompt = f"""
    Generate engaging social media posts based on the following script:

    "{script}"

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
