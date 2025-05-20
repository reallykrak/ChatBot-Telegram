import telebot
import requests
import urllib.parse

BOT_TOKEN = '8158580587:AAEOoRXYg5UCLvHKUAbFbVChDMBV-JPD4pk'  # BotFather'dan aldığın token

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = urllib.parse.quote(message.text)

    try:
        url = f"https://api.popcat.xyz/chatbot?msg={user_input}&owner=anon&botname=KüfürbazBot"
        response = requests.get(url)

        if response.status_code == 200:
            reply = response.json()["response"]
            bot.reply_to(message, reply)
        else:
            bot.reply_to(message, "API cevap vermedi.")
    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {e}")

bot.polling()
