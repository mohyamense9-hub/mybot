from telethon import TelegramClient, events
import os
import re

# ================== الإعدادات ==================
api_id = int(os.getenv("API_ID", "39864754"))
api_hash = os.getenv("API_HASH", "254da5354e8595342d963ef27049c772")

SOURCE_CHAT = -1003808609180   # جروب المصدر
TARGET_CHAT = -1003780430452   # جروبك

HEADER_TEXT = "𝚂𝙴𝙻𝚅𝙰 𝙾𝚃𝙿✨❤️‍🩹"
# ==============================================

client = TelegramClient("session", api_id, api_hash)

def is_valid_message(text: str) -> bool:
    if not text:
        return False

    # يلتقط:
    # +992★★562
    # 118-426
    # أي رقم 4 خانات أو أكتر
    patterns = [
        r"\+\d+",            # رقم يبدأ بـ +
        r"\d{4,}",           # 4 أرقام أو أكتر
        r"Code\s*:\s*\d",    # Code: مع رقم
        r"\d+-\d+"           # أرقام بشرطة
    ]

    for p in patterns:
        if re.search(p, text, re.IGNORECASE):
            return True

    return False

@client.on(events.NewMessage(chats=SOURCE_CHAT))
async def handler(event):
    try:
        text = event.message.text or event.message.caption

        if is_valid_message(text):
            final_text = f"{HEADER_TEXT}\n{text}"
            await client.send_message(TARGET_CHAT, final_text)
            print("Copied & sent")

    except Exception as e:
        print("Error:", e)

print("User script running...")
client.start()
client.run_until_disconnected()
