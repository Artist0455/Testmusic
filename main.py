import os, requests
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")

bot = Client("reelbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start"))
def start(_, msg: Message):
    msg.reply("👋 Hi! Send me an Instagram Reel link with:\n`/reel <url>`")

@bot.on_message(filters.command("reel"))
def reel_downloader(_, msg: Message):
    if len(msg.command) < 2:
        msg.reply("⚠️ Please send a reel URL.\nExample: `/reel <link>`")
        return
    
    url = msg.command[1]
    msg.reply("⏳ Downloading your reel, please wait...")

    payload = {"urls":[{"url": url}], "quality":"best"}

    r = requests.post(
        f"https://api.apify.com/v2/acts/thenetaji~instagram-video-downloader/runs?token={APIFY_API_TOKEN}",
        json=payload
    ).json()

    # response me se video link nikalna
    video_url = None
    try:
        video_url = r["data"]["input"]["urls"][0]["url"]
    except:
        pass

    if video_url:
        msg.reply_video(video_url, caption="🎬 Here is your Reel!")
    else:
        msg.reply("❌ Failed to fetch the reel. Try again later.")

bot.run()
