import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
from http.server import SimpleHTTPRequestHandler
import socketserver
import threading

# --- SECURITY KEYS (From Server Settings) ---
# We use Environment Variables so your ID is hidden from hackers
TOKEN = os.environ.get("T8503812037:AAFu6zCSez0ro9NIFJX65v2r_9MvLEiDbgQ")
# This is the new line you asked for:
ADMIN_ID = int(os.environ.get("1179345537", "0")) 
PORT = int(os.environ.get("PORT", 8080))

# --- CONFIGURATION ---
# REPLACE THIS WITH YOUR GITHUB USERNAME
WEB_APP_URL = https://github.com/arsycoxxx-cell

# --- CONTROLLER LOGIC ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    
    # 1. IDENTIFY THE USER
    if user_id == ADMIN_ID:
        # If it is YOU (The Commander)
        status_msg = "🛡️ <b>COMMANDER RECOGNIZED</b>\nAds: DISABLED\nMode: ADMIN"
        # We add '?role=admin' to the URL. The Web App reads this and hides ads.
        final_url = f"{WEB_APP_URL}?role=admin"
    else:
        # If it is a User/Guest
        status_msg = "🟢 <b>AR SYSTEM ONLINE</b>\nAccess the Interface below."
        final_url = WEB_APP_URL

    # 2. CREATE THE LAUNCH BUTTON
    keyboard = [[InlineKeyboardButton("🚀 LAUNCH INTERFACE", web_app=WebAppInfo(url=final_url))]]
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
