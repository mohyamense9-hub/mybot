from telethon import TelegramClient, events
import os
import re
import asyncio

# ================== الإعدادات ==================
api_id = int(os.getenv("API_ID", "38460443"))
api_hash = os.getenv("API_HASH", "5ee35420f38f9fe6915f3606fb353fb9")

SOURCE_CHAT = -1003808609180   # جروب المصدر
TARGET_CHAT = -1003886484488  # جروبك

HEADER_TEXT = "Collect Code✨❤️"
# ==============================================

client = TelegramClient("okay", api_id, api_hash)

# قائمة لتخزين معرفات الرسائل المرسلة حتى نحذفها لاحقًا
sent_messages = []

def is_valid_message(text: str) -> bool:
    if not text:
        return False

    patterns = [
        r"\+\d+",          # رقم يبدأ بـ +
        r"\d{4,}",         # 4 أرقام أو أكثر
        r"Code\s*:\s*\d",  # Code: مع رقم
        r"\d+-\d+"         # أرقام بشرطة
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
            msg = await client.send_message(TARGET_CHAT, final_text)
            sent_messages.append(msg.id)  # حفظ معرف الرسالة
            print("Copied & sent")
    except Exception as e:
        print("Error:", e)

async def delete_messages_periodically():
    while True:
        await asyncio.sleep(180)  # كل 3 دقائق
        if sent_messages:
            try:
                # حذف كل الرسائل المخزنة
                await client.delete_messages(TARGET_CHAT, sent_messages)
                print(f"Deleted {len(sent_messages)} messages")
                sent_messages.clear()  # تفريغ القائمة بعد الحذف
            except Exception as e:
                print("Error deleting messages:", e)

async def main():
    await client.start()
    print("User script running...")
    # تشغيل كل المهام
    await asyncio.gather(
        delete_messages_periodically(),
        client.run_until_disconnected()
    )

asyncio.run(main())
