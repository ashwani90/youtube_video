from gtts import gTTS  
import os  

text = "Welcome to today's news update. Here are the top headlines!"  
tts = gTTS(text, lang='en')  
tts.save("audio.mp3")  
os.system("start audio.mp3")  # Play the audio  


#  using eleven labs

import requests  

api_key = "your_api_key"  
text = "Breaking news! Stock markets hit an all-time high."  

response = requests.post("https://api.elevenlabs.io/v1/text-to-speech",  
    json={"text": text, "voice": "Matthew"},  
    headers={"xi-api-key": api_key})  

with open("audio.mp3", "wb") as f:  
    f.write(response.content)  
