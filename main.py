import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls, idle
from pytgcalls.types import Update
from pytgcalls.types.input_stream import InputAudioStream
from yt_dlp import YoutubeDL

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION_STRING = os.getenv("SESSION_STRING")

app = Client("music-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user = Client(SESSION_STRING, api_id=API_ID, api_hash=API_HASH)

pytg = PyTgCalls(user)

ydl_opts = {"format": "bestaudio", "noplaylist": True}

@app.on_message(filters.command("start"))
async def start(_, msg):
    await msg.reply_text("🎵 VC Music Bot is running!\nUse /play <song name or link>")

@app.on_message(filters.command("play") & filters.reply | filters.regex("play"))
async def play(_, msg):
    if len(msg.command) < 2:
        return await msg.reply_text("❌ Please give a song name or link.")

    query = " ".join(msg.command[1:])
    await msg.reply_text(f"🔎 Searching: {query}")

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        url = info["url"]

    chat_id = msg.chat.id
    await pytg.join_group_call(chat_id, InputAudioStream(url))
    await msg.reply_text(f"▶️ Playing: {info['title']}")

async def main():
    await user.start()
    await pytg.start()
    await app.start()
    print("✅ Music bot started.")
    await idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
  
