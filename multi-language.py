from googletrans import Translator

def translate_text(text, target_language="es"):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language).text
    return translated_text

# Example Usage
TEXT_CONTENT = "Breaking news! The stock market has reached an all-time high."
translated_text = translate_text(TEXT_CONTENT, "fr")  # Translate to French
print("✔ Translated Script:", translated_text)

translated_text = translate_text(TEXT_CONTENT, "fr")  # Translate to French
generate_audio(translated_text, AUDIO_FILE)  # Generate voiceover in French
