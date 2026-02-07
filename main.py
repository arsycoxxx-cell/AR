import os, telebot, requests, time, threading
from flask import Flask, request

# IDENTITY & CREDENTIALS
API_TOKEN = '8503812037:AAFu6zCSez0ro9NIFJX65v2r_9MvLEiDbgQ'
TMDB_API = '19241042e5671d4369263a2b6f8e7ff5'
CHANNEL_ID = "@ar_downloader"
HUB_URL = "https://arsycoxxx-cell.github.io/AR/index.html"

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

def auto_poster():
    time.sleep(10) # 10s delay after deployment
    while True:
        try:
            url = f"https://api.themoviedb.org/3/trending/all/day?api_key={TMDB_API}"
            items = requests.get(url).json().get('results', [])
            for item in items:
                title = item.get('title') or item.get('name')
                # Connection: Encodes title for the 4-stage search hub
                link = f"{HUB_URL}?q={requests.utils.quote(title)}"
                post = f"🔥 **NEW RELEASE** 🔥\n\n🎬 **{title}**\n\n📥 **DOWNLOAD:**\n{link}"
                bot.send_message(CHANNEL_ID, post, parse_mode="Markdown")
                time.sleep(3600) # One post every hour
        except: time.sleep(60)

@app.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://ar-9yvx.onrender.com/' + API_TOKEN) #
    return "AR_EMPIRE_LIVE", 200

if __name__ == "__main__":
    threading.Thread(target=auto_poster).start()
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 10000))) #
