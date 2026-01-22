import os, requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = os.environ["BOT_TOKEN"]
WEBAPP_URL = os.environ["WEBAPP_URL"]

def parse_msg(text: str):
    parts = [p.strip() for p in text.split("|")]
    while len(parts) < 6:
        parts.append("")
    return {
        "ma": parts[0],
        "name": parts[1],
        "uid": parts[2],
        "ghi_chu": parts[3],
        "link_fake": parts[4],
        "link_fake2": parts[5],
    }

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (update.message.text or "").strip()
    if "|" not in msg:
        await update.message.reply_text("Nhắn đúng format: MA | NAME | UID | GHI CHU | LINK FAKE | LINK FAKE2")
        return

    data = parse_msg(msg)
    r = requests.post(WEBAPP_URL, json=data, timeout=15)

    if r.status_code == 200:
        await update.message.reply_text("✅ Đã ghi vào Sheet!")
    else:
        await update.message.reply_text("❌ Lỗi ghi Sheet")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.run_polling()

if __name__ == "__main__":
    main()
