from gtts import gTTS  
import os  

text = "Welcome to today's news update. Here are the top headlines!"  
tts = gTTS(text, lang='en')  
tts.save("audio.mp3")  
os.system("start audio.mp3")  # Play the audio  
