import os
import telebot
from flask import Flask, request

# IDENTITY DATA
API_TOKEN = '8503812037:AAFu6zCSez0ro9NIFJX65v2r_9MvLEiDbgQ' 
bot = telebot.TeleBot(API_TOKEN)
server = Flask(__name__)

ADMIN_ID = 1179345537
CHANNEL_ID = "@ar_downloader" 
HUB_URL = "https://arsycoxxx-cell.github.io/AR/index.html"

@bot.message_handler(commands=['start'])
def start(message):
    # Greeting as AR Syco
    text = "SYSTEM_ACCESS: AR Syco v4.0. Join @ar_downloader to unlock the Master Sheet."
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("📢 JOIN CHANNEL", url="https://t.me/ar_downloader"))
    bot.send_message(message.chat.id, text, reply_markup=markup)

@server.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://ar-9yvx.onrender.com/' + API_TOKEN) #
    return "AR_EMPIRE_LIVE", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 10000))) #
