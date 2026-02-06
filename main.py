import os, threading, socketserver, asyncio, requests, json, random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ChatMemberStatus

# --- [ 1. EMPIRE CONFIGURATION (Hardcoded for You) ] ---
# I fixed the syntax so these work immediately without Render Environment Variables.
TOKEN = "8503812037:AAFu6zCSez0ro9NIFJX65v2r_9MvLEiDbgQ"
ADMIN_ID = 1179345537
CHANNEL_ID = "@ar_downloader"
APP_URL = "https://arsycoxxx-cell.github.io/AR/"
TMDB_KEY = "19241042e5671d4369263a2b6f8e7ff5"
NEWS_KEY = "pub_114d737697a4438e977f933d8342f495"

# --- [ 2. SELF-HEALING & SCRAPER ENGINES ] ---
def fetch_anime_donghua():
    # Jikan API for Anime/Donghua Schedules
    try:
        url = "https://api.jikan.moe/v4/schedules/now"
        data = requests.get(url).json()['data']
        # Sort by popularity to get the best hits
        return sorted(data, key=lambda x: x['popularity'])[:2]
    except: return []

def fetch_movies():
    # TMDB for Movies/Web Series
    try:
        url = f"https://api.themoviedb.org/3/trending/all/day?api_key={TMDB_KEY}"
        data = requests.get(url).json()['results'][:2]
        return data
    except: return []

# --- [ 3. THE AUTONOMOUS GHOST WRITER ] ---
async def auto_post_loop(context: ContextTypes.DEFAULT_TYPE):
    # Runs continuously to fill your channel with content
    while True:
        try:
            # 1. POST ANIME/DONGHUA
            anime_list = fetch_anime_donghua()
            for item in anime_list:
                title = item['title']
                img = item['images']['jpg']['large_image_url']
                # DEEP LINK: Encodes the title so the App knows what to search
                safe_title = title.replace(" ", "_")
                
                caption = (
                    f"🏮 <b>NEW RELEASE: {title}</b>\n"
                    f"⚡ <i>Status:</i> AIRING NOW\n"
                    f"📡 <i>Source:</i> 4K/1080p\n\n"
                    f"👇 <b>CLICK TO WATCH & DOWNLOAD</b>"
                )
                # CONNECTS CHANNEL TO DASHBOARD AUTO-SEARCH
                btn = [[InlineKeyboardButton("📥 DOWNLOAD EPISODE", web_app=WebAppInfo(url=f"{APP_URL}?startapp=search_{safe_title}"))]]
                await context.bot.send_photo(chat_id=CHANNEL_ID, photo=img, caption=caption, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(btn))
                await asyncio.sleep(1200) # 20 mins between posts

            # 2. POST MOVIES/WEB SERIES
            movie_list = fetch_movies()
            for item in movie_list:
                name = item.get('title', item.get('name'))
                img = f"https://image.tmdb.org/t/p/w500{item['poster_path']}"
                safe_name = name.replace(" ", "_")
                
                caption = (
                    f"🎥 <b>PREMIERE: {name}</b>\n"
                    f"🌟 <i>Rating:</i> {item['vote_average']}/10\n"
                    f"⚡ <i>Quality:</i> WEB-DL / 4K\n\n"
                    f"👇 <b>CLICK TO WATCH & DOWNLOAD</b>"
                )
                btn = [[InlineKeyboardButton("📥 DOWNLOAD MOVIE", web_app=WebAppInfo(url=f"{APP_URL}?startapp=search_{safe_name}"))]]
                await context.bot.send_photo(chat_id=CHANNEL_ID, photo=img, caption=caption, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(btn))
                await asyncio.sleep(1200)

            await asyncio.sleep(14400) # Sleep 4 Hours then repeat
        except Exception as e:
            print(f"Auto-Heal Triggered: {e}") # Silent error handling
            await asyncio.sleep(60)

# --- [ 4. THE CONTROLLER & AD GUARD ] ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args
    
    # 1. SUBSCRIPTION GATE (Join-to-Use)
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user.id)
        if member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED]:
            btn = [[InlineKeyboardButton("📢 JOIN CHANNEL TO UNLOCK", url=f"https://t.me/{CHANNEL_ID.replace('@', '')}")]]
            await update.message.reply_text("❌ ACCESS DENIED! Join the channel to use the AR App.", reply_markup=InlineKeyboardMarkup(btn))
            return
    except: pass
    
    # 2. ADMIN AD-GUARD CHECK
    if user.id == ADMIN_ID:
        role = "admin"
        status = "🛡️ <b>COMMANDER MODE</b>\nAds: DISABLED\nSystem: UNLOCKED"
    else:
        role = "user"
        status = "⚡ <b>AR SYCO SYSTEM</b>\nAds: ACTIVE\nAccess: GRANTED"

    # 3. CONTEXT AWARENESS (Deep Linking)
    payload = args[0] if args else "dashboard"
    final_url = f"{APP_URL}?role={role}&task={payload}"

    keyboard = [
        [InlineKeyboardButton("🚀 LAUNCH DASHBOARD", web_app=WebAppInfo(url=final_url))],
        [InlineKeyboardButton("🌐 SEARCH ARCHIVE", url=final_url)]
    ]
    await update.message.reply_html(status, reply_markup=InlineKeyboardMarkup(keyboard))

# --- [ 5. SERVER KEEPALIVE ] ---
def run_server():
    # This keeps Render running for free
    port = int(os.environ.get("PORT", 8080))
    with socketserver.TCPServer(("", port), socketserver.SimpleHTTPRequestHandler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    # Activate the Auto-Poster
    if CHANNEL_ID:
        app.job_queue.run_once(auto_post_loop, 10)
        
    print("AR SYCO MONOLITH ONLINE")
    app.run_polling()
            # 1. POST ANIME/DONGHUA
            anime_list = fetch_anime_donghua()
            for item in anime_list:
                title = item['title']
                img = item['images']['jpg']['large_image_url']
                # DEEP LINK: Encodes the title so the App knows what to search
                safe_title = title.replace(" ", "_")
                
                caption = (
                    f"🏮 <b>NEW RELEASE: {title}</b>\n"
                    f"⚡ <i>Status:</i> AIRING NOW\n"
                    f"📡 <i>Source:</i> 4K/1080p\n\n"
                    f"👇 <b>CLICK TO WATCH & DOWNLOAD</b>"
                )
                # CONNECTS CHANNEL TO DASHBOARD AUTO-SEARCH
                btn = [[InlineKeyboardButton("📥 DOWNLOAD EPISODE", web_app=WebAppInfo(url=f"{APP_URL}?startapp=search_{safe_title}"))]]
                await context.bot.send_photo(chat_id=CHANNEL_ID, photo=img, caption=caption, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(btn))
                await asyncio.sleep(1200) # 20 mins between posts

            # 2. POST MOVIES/WEB SERIES
            movie_list = fetch_movies()
            for item in movie_list:
                name = item.get('title', item.get('name'))
                img = f"https://image.tmdb.org/t/p/w500{item['poster_path']}"
                safe_name = name.replace(" ", "_")
                
                caption = (
                    f"🎥 <b>PREMIERE: {name}</b>\n"
                    f"🌟 <i>Rating:</i> {item['vote_average']}/10\n"
                    f"⚡ <i>Quality:</i> WEB-DL / 4K\n\n"
                    f"👇 <b>CLICK TO WATCH & DOWNLOAD</b>"
                )
                btn = [[InlineKeyboardButton("📥 DOWNLOAD MOVIE", web_app=WebAppInfo(url=f"{APP_URL}?startapp=search_{safe_name}"))]]
                await context.bot.send_photo(chat_id=CHANNEL_ID, photo=img, caption=caption, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(btn))
                await asyncio.sleep(1200)

            await asyncio.sleep(14400) # Sleep 4 Hours then repeat
        except Exception as e:
            print(f"Auto-Heal Triggered: {e}") # Silent error handling
            await asyncio.sleep(60)

# --- [ 4. THE CONTROLLER & AD GUARD ] ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args
    
    # CONTEXT AWARENESS: Did they come from a specific search?
    # If they clicked a link like t.me/bot?start=naruto, the app opens searching for Naruto.
    payload = args[0] if args else "dashboard"

    # ADMIN AD-GUARD: Checks if it is YOU
    if user.id == ADMIN_ID:
        role = "admin"
        status = "🛡️ <b>COMMANDER MODE</b>\nAds: DISABLED\nSystem: UNLOCKED"
    else:
        role = "user"
        status = "⚡ <b>AR SYCO SYSTEM</b>\nAds: ACTIVE\nAccess: GRANTED"

    # GENERATE SMART LINK
    final_url = f"{APP_URL}?role={role}&task={payload}"

    keyboard = [
        [InlineKeyboardButton("🚀 LAUNCH DASHBOARD", web_app=WebAppInfo(url=final_url))],
        [InlineKeyboardButton("🌐 SEARCH ARCHIVE", url=final_url)]
    ]
    await update.message.reply_html(status, reply_markup=InlineKeyboardMarkup(keyboard))

# --- [ 5. SERVER KEEPALIVE ] ---
def run_server():
    port = int(os.environ.get("PORT", 8080))
    with socketserver.TCPServer(("", port), socketserver.SimpleHTTPRequestHandler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    # Activate the Auto-Poster
    if CHANNEL_ID:
        app.job_queue.run_once(auto_post_loop, 10)
        
    print("AR SYCO MONOLITH ONLINE")
    app.run_polling()
            # 1. POST ANIME/DONGHUA
            anime_list = fetch_anime_donghua()
            for item in anime_list:
                title = item['title']
                img = item['images']['jpg']['large_image_url']
                # DEEP LINK: Encodes the title so the App knows what to search
                safe_title = title.replace(" ", "_")
                
                caption = (
                    f"🏮 <b>NEW RELEASE: {title}</b>\n"
                    f"⚡ <i>Status:</i> AIRING NOW\n"
                    f"📡 <i>Source:</i> 4K/1080p\n\n"
                    f"👇 <b>CLICK TO WATCH & DOWNLOAD</b>"
                )
                # CONNECTS CHANNEL TO DASHBOARD AUTO-SEARCH
                btn = [[InlineKeyboardButton("📥 DOWNLOAD EPISODE", web_app=WebAppInfo(url=f"{APP_URL}?startapp=search_{safe_title}"))]]
                await context.bot.send_photo(chat_id=CHANNEL_ID, photo=img, caption=caption, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(btn))
                await asyncio.sleep(1200) # 20 mins between posts

            # 2. POST MOVIES/WEB SERIES
            movie_list = fetch_movies()
            for item in movie_list:
                name = item.get('title', item.get('name'))
                img = f"https://image.tmdb.org/t/p/w500{item['poster_path']}"
                safe_name = name.replace(" ", "_")
                
                caption = (
                    f"🎥 <b>PREMIERE: {name}</b>\n"
                    f"🌟 <i>Rating:</i> {item['vote_average']}/10\n"
                    f"⚡ <i>Quality:</i> WEB-DL / 4K\n\n"
                    f"👇 <b>CLICK TO WATCH & DOWNLOAD</b>"
                )
                btn = [[InlineKeyboardButton("📥 DOWNLOAD MOVIE", web_app=WebAppInfo(url=f"{APP_URL}?startapp=search_{safe_name}"))]]
                await context.bot.send_photo(chat_id=CHANNEL_ID, photo=img, caption=caption, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(btn))
                await asyncio.sleep(1200)

            await asyncio.sleep(14400) # Sleep 4 Hours then repeat
        except Exception as e:
            print(f"Auto-Heal Triggered: {e}") # Silent error handling
            await asyncio.sleep(60)

# --- [ 4. THE CONTROLLER & AD GUARD ] ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args
    
    # CONTEXT AWARENESS: Did they come from a specific search?
    # If they clicked a link like t.me/bot?start=naruto, the app opens searching for Naruto.
    payload = args[0] if args else "dashboard"

    # ADMIN AD-GUARD: Checks if it is YOU
    if user.id == ADMIN_ID:
        role = "admin"
        status = "🛡️ <b>COMMANDER MODE</b>\nAds: DISABLED\nSystem: UNLOCKED"
    else:
        role = "user"
        status = "⚡ <b>AR SYCO SYSTEM</b>\nAds: ACTIVE\nAccess: GRANTED"

    # GENERATE SMART LINK
    final_url = f"{APP_URL}?role={role}&task={payload}"

    keyboard = [
        [InlineKeyboardButton("🚀 LAUNCH DASHBOARD", web_app=WebAppInfo(url=final_url))],
        [InlineKeyboardButton("🌐 SEARCH ARCHIVE", url=final_url)]
    ]
    await update.message.reply_html(status, reply_markup=InlineKeyboardMarkup(keyboard))

# --- [ 5. SERVER KEEPALIVE ] ---
def run_server():
    port = int(os.environ.get("PORT", 8080))
    with socketserver.TCPServer(("", port), socketserver.SimpleHTTPRequestHandler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    # Activate the Auto-Poster
    if CHANNEL_ID:
        app.job_queue.run_once(auto_post_loop, 10)
        
    print("AR SYCO MONOLITH ONLINE")
    app.run_polling()
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_html(status_msg, reply_markup=reply_markup)

# --- WEB SERVER (Keeps Bot Alive for Free) ---
def run_web_server():
    class HealthCheckHandler(SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"AR System Controller Active")
    with socketserver.TCPServer(("", PORT), HealthCheckHandler) as httpd:
        httpd.serve_forever()

# --- MAIN EXECUTION ---
def main():
    threading.Thread(target=run_web_server, daemon=True).start()
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == "__main__":
    main()
