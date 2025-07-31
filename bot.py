import telebot
import requests
import base64
import os
from io import BytesIO

BOT_TOKEN = '8456728583:AAGVjaFzVdCrZuXSNrL7w0OQucdaZpYqmI0'
GEMINI_API_KEY = 'AIzaSyDGXakapXgul46kbkC6P4RI-yObnzeFsgM'  # Google Gemini API key

bot = telebot.TeleBot(BOT_TOKEN)

# Google Gemini chat API sorgusu
def gemini_query(user_input):
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={GEMINI_API_KEY}'
    system_instruction = """
    Sen üst düzey yazılım ve yapay zekâ asistanısın.
    Her zaman Türkçe cevap ver.
    Kullanıcı kod yazmanı isterse, güncel ve profesyonel Python kodu yaz.
    Fotoğraf gönderildiğinde analiz et ve açıklama yap.
    Cevaplarını doğal ve güzel bir robot sesiyle seslendirmek için hazırla.
    """
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": system_instruction},
                    {"text": user_input}
                ]
            }
        ]
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"API hatası: {response.status_code}"

# Sesli yanıt oluşturma (StreamElements TTS API)
def generate_voice(text):
    tts_url = "https://api.streamelements.com/kappa/v2/speech"
    params = {
        "voice": "Brian",  # Doğal ve güzel robot sesi
        "text": text
    }
    response = requests.get(tts_url, params=params)
    if response.status_code == 200:
        voice_path = "response.mp3"
        with open(voice_path, "wb") as f:
            f.write(response.content)
        return voice_path
    return None

# Fotoğrafı analiz etmek için basit örnek (Google Vision API veya başka hizmet entegre edilebilir)
def analyze_photo(file_bytes):
    # Şimdilik basit placeholder, dosya boyutunu döner
    size_kb = len(file_bytes) / 1024
    return f"Fotoğraf alındı. Boyutu yaklaşık {size_kb:.2f} KB."

@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_input = message.text
    reply = gemini_query(user_input)
    bot.reply_to(message, reply)

    voice_file = generate_voice(reply)
    if voice_file:
        with open(voice_file, 'rb') as audio:
            bot.send_voice(message.chat.id, audio)
        os.remove(voice_file)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file_data = bot.download_file(file_info.file_path)

        # Fotoğraf analiz et
        analysis_result = analyze_photo(file_data)
        bot.reply_to(message, analysis_result)

        # Sesli yanıt
        voice_file = generate_voice(analysis_result)
        if voice_file:
            with open(voice_file, 'rb') as audio:
                bot.send_voice(message.chat.id, audio)
            os.remove(voice_file)
    except Exception as e:
        bot.reply_to(message, f"Fotoğraf işlenirken hata oluştu: {e}")

bot.polling()
