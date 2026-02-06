import os
import threading
import socketserver
import http.server  # <--- ADDED THIS FIXED IMPORT
import asyncio
import requests
import json
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ChatMemberStatus

# --- [ 1. EMPIRE CONFIGURATION ] ---
TOKEN = "8503812037:AAFu6zCSez0ro9NIFJX65v2r_9MvLEiDbgQ"
ADMIN_ID = 1179345537
CHANNEL_ID = "@ar_downloader"
APP_URL = "https://arsycoxxx-cell.github.io/"
TMDB_KEY = "19241042e5671d4369263a2b6f8e7ff5"
NEWS_KEY = "pub_114d737697a4438e977f933d8342f495"

# --- [ 2. SELF-HEALING & SCRAPER ENGINES ] ---
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

# --- [ 3. THE AUTONOMOUS GHOST WRITER ] ---
async def auto_post_loop(context: ContextTypes.DEFAULT_TYPE):
    while True:
        try:
            # 1. POST ANIME
            anime_list = fetch_anime_donghua()
            for item in anime_list:
                title = item['title']
                try:
                    img = item['images']['jpg']['large_image_url']
                except: continue
                
                safe_title = title.replace(" ", "_")
                caption = (
                    f"🏮 <b>NEW RELEASE: {title}</b>\n"
                    f"⚡ <i>Status:</i> AIRING NOW\n"
                    f"📡 <i>Source:</i> 4K/1080p\n\n"
                    f"👇 <b>CLICK TO WATCH & DOWNLOAD</b>"
                )
                btn = [[InlineKeyboardButton("📥 DOWNLOAD EPISODE", web_app=WebAppInfo(url=f"{APP_URL}?startapp=search_{safe_title}"))]]
                await context.bot.send_photo(chat_id=CHANNEL_ID, photo=img, caption=caption, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(btn))
                await asyncio.sleep(1200)

            # 2. POST MOVIES
            movie_list = fetch_movies()
            for item in movie_list:
                name = item.get('title', item.get('name'))
                if not name: continue
                try:
                    img = f"https://image.tmdb.org/t/p/w500{item['poster_path']}"
                except: continue
                
                safe_name = name.replace(" ", "_")
                caption = (
                    f"🎥 <b>PREMIERE: {name}</b>\n"
                    f"🌟 <i>Rating:</i> {item.get('vote_average', 'N/A')}/10\n"
                    f"⚡ <i>Quality:</i> WEB-DL / 4K\n\n"
                    f"👇 <b>CLICK TO WATCH & DOWNLOAD</b>"
                )
                btn = [[InlineKeyboardButton("📥 DOWNLOAD MOVIE", web_app=WebAppInfo(url=f"{APP_URL}?startapp=search_{safe_name}"))]]
                await context.bot.send_photo(chat_id=CHANNEL_ID, photo=img, caption=caption, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(btn))
                await asyncio.sleep(1200)

            await asyncio.sleep(14400)
        except Exception as e:
            print(f"Auto-Heal Error: {e}")
            await asyncio.sleep(60)

# --- [ 4. THE CONTROLLER ] ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args
    
    # Context & Admin Check
    payload = args[0] if args else "dashboard"
    if user.id == ADMIN_ID:
        role = "admin"
        status = "🛡️ <b>COMMANDER MODE</b>\nAds: DISABLED"
    else:
        role = "user"
        status = "⚡ <b>AR SYCO SYSTEM</b>\nAds: ACTIVE"

    final_url = f"{APP_URL}?role={role}&task={payload}"
    keyboard = [[InlineKeyboardButton("🚀 LAUNCH DASHBOARD", web_app=WebAppInfo(url=final_url))]]
    await update.message.reply_html(status, reply_markup=InlineKeyboardMarkup(keyboard))

# --- [ 5. SERVER KEEPALIVE ] ---
def run_server():
    port = int(os.environ.get("PORT", 8080))
    # FIXED: Used http.server instead of socketserver for the handler
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"Serving on port {port}")
        httpd.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    if CHANNEL_ID:
        app.job_queue.run_once(auto_post_loop, 10)
        
    print("AR SYCO MONOLITH ONLINE")
    app.run_polling()
