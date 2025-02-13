import requests

ELEVENLABS_API_KEY = "your-elevenlabs-api-key"
VOICE_ID = "pNInz6obpgDQGcFmaJgB"  # Choose a voice from ElevenLabs
AUDIO_FILE = "audio.mp3"

def generate_audio(text, output_file):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.6, "similarity_boost": 0.85}
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(response.content)
        print("✔ High-quality AI voice generated!")
    else:
        print("❌ Error generating voice:", response.json())

# Example usage:
TEXT_CONTENT = "Breaking news! The stock market has reached an all-time high. Experts predict continued growth in the coming months."
generate_audio(TEXT_CONTENT, AUDIO_FILE)
