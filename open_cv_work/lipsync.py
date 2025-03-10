import librosa

def match_lip_sync(audio_file):
    y, sr = librosa.load(audio_file)
    energy = librosa.feature.rms(y=y)
    
    # Use energy levels to determine mouth open/close
    mouth_states = ["open" if e > 0.02 else "closed" for e in energy[0]]
    
    return mouth_states


