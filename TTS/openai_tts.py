import os
import time
import openai

from text import news_en, news_fr, news_ch, story_en, story_fr, story_ch

def load_openai_key():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    key_path = os.path.join(project_root, "config", "OpenAI_Key.txt")

    try:
        with open(key_path, "r", encoding="utf-8") as f:
            key = f.read().strip()
        return key
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {key_path}")

# Load OpenAI API key
openai.api_key = load_openai_key()

# Ensure output directory exists
project_root = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(project_root, "output")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Texts to be converted to speech
texts = {
    "news_en": news_en,
    "news_fr": news_fr,
    "news_ch": news_ch,
    "story_en": story_en,
    "story_fr": story_fr,
    "story_ch": story_ch,
}

# Models to be used
models = {
    "tts": "tts-1",
    "ttshd": "tts-1-hd",
}

# Voice mapping based on content type
voice_map = {
    "news": "alloy",
    "story": "fable"
}

# Generate speech for each text and model combination
for text_key, text_value in texts.items():
    voice = voice_map["news"] if "news" in text_key else voice_map.get("story", "alloy")

    for model_key, model_name in models.items():
        print(f"Generating speech for {text_key} using model {model_name} (voice: {voice})...")
        try:
            start_time = time.time()

            # Generate speech using OpenAI API
            response = openai.audio.speech.create(
                model=model_name,
                input=text_value,
                voice=voice
            )

            elapsed = round(time.time() - start_time)  # Round elapsed time to seconds
            print(f"Speech generation for {text_key} took: {elapsed} seconds")

            # Count tokens (simple word count, can be replaced with more accurate tokenization)
            token_count = len(text_value.split())

            # Save the generated audio file
            filename = f"openai_{model_key}_{text_key}_{elapsed}s_{token_count}tokens.mp3"
            filepath = os.path.join(output_dir, filename)

            with open(filepath, "wb") as audio_file:
                audio_file.write(response.content)
            print(f"File saved: {filepath}\n")

        except Exception as e:
            print(f"Error generating speech for {text_key} (model: {model_name}, voice: {voice}): {e}\n")
