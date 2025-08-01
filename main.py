from pyrogram import Client, filters
import os
import re

API_ID = int(os.getenv("22182189"))
API_HASH = os.getenv("5e7c4088f8e23d0ab61e29ae11960bf5")
BOT_TOKEN = os.getenv("7192614101:AAFUo1ostxyYRNFWm_zkxMpT-AlIkXdiIoI")

bot = Client("sh_to_txt_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.document)
async def handle_doc(bot, message):
    file_path = await message.download()
    clean_lines = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            match = re.match(r"(.+?\.(mp4|pdf|mkv))[:\-\s]+(https?://\S+)", line)
            if match:
                name, ext, url = match.groups()
                clean_lines.append(f"File Name: {name}\nURL: {url}\n")

    if not clean_lines:
        await message.reply("⚠️ Koi valid links nahi mile.")
        return

    output_path = "converted_clean.txt"
    with open(output_path, "w", encoding="utf-8") as out:
        out.write("\n".join(clean_lines))

    await message.reply_document(output_path, caption="✅ Cleaned & Extracted URLs")
    os.remove(file_path)
    os.remove(output_path)

bot.run()
