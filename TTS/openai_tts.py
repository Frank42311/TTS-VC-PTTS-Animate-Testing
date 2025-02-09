import os
import time
import openai

from text import news_en, news_fr, story_en, story_fr

def load_openai_key():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    key_path = os.path.join(project_root, "config", "OpenAI_Key.txt")

    try:
        with open(key_path, "r", encoding="utf-8") as f:
            key = f.read().strip()
        return key
    except FileNotFoundError:
        raise FileNotFoundError(f"无法找到配置文件：{key_path}")

openai.api_key = load_openai_key()

project_root = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(project_root, "output")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

texts = {
    "news_en": news_en,
    "news_fr": news_fr,
    "story_en": story_en,
    "story_fr": story_fr,
}

models = {
    "tts": "tts-1",
    "ttshd": "tts-1-hd",
}

voice_map = {
    "news": "alloy",
    "story": "fable"
}

for text_key, text_value in texts.items():
    voice = voice_map["news"] if "news" in text_key else voice_map.get("story", "alloy")

    for model_key, model_name in models.items():
        print(f"开始生成 {text_key} 使用模型 {model_name}（声音：{voice}）的语音...")
        try:
            start_time = time.time()

            # 使用新版 API
            response = openai.audio.speech.create(
                model=model_name,
                input=text_value,
                voice=voice
            )

            elapsed = round(time.time() - start_time)  # 四舍五入到秒
            print(f"生成 {text_key} 的语音耗时：{elapsed} 秒")

            # 计算 token 数量
            token_count = len(text_value.split())  # 简单按空格分词计数，可替换为更精确的 token 计算方法

            filename = f"openai_{model_key}_{text_key}_{elapsed}s_{token_count}tokens.mp3"
            filepath = os.path.join(output_dir, filename)

            with open(filepath, "wb") as audio_file:
                audio_file.write(response.content)
            print(f"已保存文件：{filepath}\n")

        except Exception as e:
            print(f"生成 {text_key} 语音时出错（模型：{model_name}，声音：{voice}）：{e}\n")
