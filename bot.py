import telebot
import requests
import urllib.parse

BOT_TOKEN = '8158580587:AAEOoRXYg5UCLvHKUAbFbVChDMBV-JPD4pk'  # Bot tokenini buraya yaz
bot = telebot.TeleBot(BOT_TOKEN)

API_URL = "https://z4aher.totalh.net/gemini/GeminiChat.php?prompt="

# Özel cevaplar
custom_replies = {
    "hile ne zaman çıkacak": "Çıkmaz ayın çarşambasında çıkacak gardaş, bekle babana da söyleriz!",
    "oyun neden çöktü": "Oyunu senin gibiler yüzünden kapattık la, rahat mısın!",
    "admin kim": "Admin benim lan! Sıkıntı mı var, hadi başka kapıya."
}

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text.lower().strip()

    # Eğer özel cevap varsa
    if user_input in custom_replies:
        bot.reply_to(message, custom_replies[user_input])
        return

    # Normal API isteği
    try:
        encoded_input = urllib.parse.quote(user_input)
        response = requests.get(API_URL + encoded_input)

        if response.status_code == 200:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "API'den cevap alınamadı.")
    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {e}")

bot.polling()
