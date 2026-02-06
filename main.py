import os
import threading
import socketserver
import http.server
import asyncio
import requests
import json
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ChatMemberStatus

# --- [ 1. CONFIGURATION ] ---
TOKEN = "8503812037:AAFu6zCSez0ro9NIFJX65v2r_9MvLEiDbgQ"
ADMIN_ID = 1179345537
CHANNEL_ID = "@ar_downloader"
APP_URL = "https://arsycoxxx-cell.github.io/AR/"
TMDB_KEY = "19241042e5671d4369263a2b6f8e7ff5"

# --- [ 2. SCRAPERS ] ---
def fetch_anime_donghua():
    try:
        url = "https://api.jikan.moe/v4/schedules/now"
        data = requests.get(url).json()['data']
        return sorted(data, key=lambda x: x['popularity'])[:2]
    except: return []

def fetch_movies():
    try:
        url = f"https://api.themoviedb.org/3/trending/all/day?api_key={TMDB_KEY}"
        data = requests.get(url).json()['results'][:2]
        return data
    except: return []

# --- [ 3. AUTO-POSTING ] ---
async def auto_post_loop(context: ContextTypes.DEFAULT_TYPE):
    while True:
        try:
            # Post Anime
            anime_list = fetch_anime_donghua()
            for item in anime_list:
                title, img = item['title'], item['images']['jpg']['large_image_url']
                safe_title = title.replace(" ", "_")
                caption = f"🏮 <b>NEW RELEASE: {title}</b>\n👇 <b>CLICK TO DOWNLOAD</b>"
                btn = [[InlineKeyboardButton("📥 DOWNLOAD", web_app=WebAppInfo(url=f"{APP_URL}?startapp=search_{safe_title}"))]]
                await context.bot.send_photo(chat_id=CHANNEL_ID, photo=img, caption=caption, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(btn))
                await asyncio.sleep(600)

            # Post Movies
            movie_list = fetch_movies()
            for item in movie_list:
                name = item.get('title', item.get('name'))
                img = f"https://image.tmdb.org/t/p/w500{item['poster_path']}"
                safe_name = name.replace(" ", "_")
                caption = f"🎥 <b>PREMIERE: {name}</b>\n👇 <b>CLICK TO DOWNLOAD</b>"
                btn = [[InlineKeyboardButton("📥 DOWNLOAD", web_app=WebAppInfo(url=f"{APP_URL}?startapp=search_{safe_name}"))]]
                await context.bot.send_photo(chat_id=CHANNEL_ID, photo=img, caption=caption, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(btn))
                await asyncio.sleep(600)

            await asyncio.sleep(14400)
        except: await asyncio.sleep(60)

# --- [ 4. CONTROLLER ] ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        # HIDE BOT FROM NON-SUBSCRIBERS
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED]:
            await update.message.reply_text(f"❌ ACCESS DENIED! Please join {CHANNEL_ID} to use the Empire App.")
            return
    except: return

    payload = context.args[0] if context.args else "dashboard"
    role = "admin" if user_id == ADMIN_ID else "user"
    final_url = f"{APP_URL}?role={role}&task={payload}"
    keyboard = [[InlineKeyboardButton("🚀 LAUNCH DASHBOARD", web_app=WebAppInfo(url=final_url))]]
    await update.message.reply_html("⚡ <b>AR SYCO SYSTEM ONLINE</b>", reply_markup=InlineKeyboardMarkup(keyboard))

# --- [ 5. SERVER ] ---
def run_server():
    port = int(os.environ.get("PORT", 8080))
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    if CHANNEL_ID:
        app.job_queue.run_once(auto_post_loop, 10)
    print("AR SYCO MONOLITH ONLINE")
    app.run_polling()
