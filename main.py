from pyrogram import Client, filters
import re
import os

api_id = int(os.getenv("8327438764"))
api_hash = os.getenv("f4303b629cb74e168e13c6a57b02c27a")
bot_token = os.getenv("7953569430:AAEUMMKOO-q2RuzvgSUiBvzO9As8IxAwtcY")

DEST = os.getenv("chanel907")          # مثلا: mydestchannel
SIGNATURE = os.getenv("@chanel907")        # مثلا: @MyDestChannel

app = Client("newsbot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

source_channel = None

def has_link(text: str):
    if not text:
        return False
    return bool(re.search(r"https?://|www\.", text))

def clean_text(text: str):
    if not text:
        return ""

    text = text.replace("@AkhbarTelFori", "")
    text = text.strip()
    return f"{text}\n\n{SIGNATURE}"

@app.on_message(filters.private & filters.command("setsource"))
async def set_source(client, message):
    global source_channel

    if len(message.command) < 2:
        await message.reply("❗ مثال:\n/setsource source_channel")
        return

    source_channel = message.command[1].replace("@", "")
    await message.reply(f"✅ کانال منبع تنظیم شد روی: {source_channel}")

@app.on_message(filters.channel)
async def handle_channel(client, message):
    global source_channel

    if not source_channel:
        return

    if not message.chat.username or message.chat.username.lower() != source_channel.lower():
        return

    # فوروارد؟
    if message.forward_from or message.forward_from_chat:
        return

    # دکمه شیشه‌ای؟
    if message.reply_markup:
        return

    text = message.text or message.caption or ""

    # لینک؟
    if has_link(text):
        return

    new_text = clean_text(text)

    try:
        if message.text:
            await app.send_message(DEST, new_text)
        else:
            await message.copy(
                chat_id=DEST,
                caption=new_text,
                reply_markup=None
            )
    except Exception as e:
        print("ERROR:", e)

app.run()
