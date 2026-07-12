import os
import asyncio
import re
from telethon import TelegramClient, events

# مقادیر دریافتی از اطلاعات شما
API_ID = 38386228
API_HASH = '4e787e48c8b9faf1dd2f44249c64c841'

# کانال‌های مبدأ
SOURCE_CHANNELS = ['@filembad']

# کانال مقصد شما
TARGET_CHANNEL = '@npv_proxy7'

# پیدا کردن مسیر دقیق پوشه اصلی روی سرور رندر برای خواندن فایل سشن
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSION_PATH = os.path.join(BASE_DIR, 'proxy_session.session')

print(f"بررسی وجود فایل سشن در مسیر: {SESSION_PATH}")
if os.path.exists(SESSION_PATH):
    print("فایل سشن با موفقیت پیدا شد.")
else:
    print("هشدار: فایل سشن در این مسیر پیدا نشد!")

# ساخت کلاینت تلگرام با آدرس دقیق فایل سشن
client = TelegramClient(os.path.splitext(SESSION_PATH)[0], API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    message_text = event.message.message
    if not message_text:
        return
        
    # ۱. جایگزین کردن آیدی کانال مبدا با کانال شما در کل متن
    new_message = message_text.replace('@filembad', '@npv_proxy7')
    
    # ۲. پیدا کردن لینک‌های پروکسی در متن پیام برای تغییر اسم انتهای لینک
    urls = re.findall(r'(t\.me/proxy\?\S+|tg://proxy\?\S+)', new_message)
    
    if urls:
        for url in urls:
            if '#' in url:
                base_url = url.split('#')[0]
            else:
                base_url = url
            
            # قرار دادن اسم کانال شما در انتهای لینک پروکسی
            new_url = f"{base_url}#@npv_proxy7"
            new_message = new_message.replace(url, new_url)
        
    try:
        # ارسال پیام ویرایش شده نهایی به کانال مقصد
        await client.send_message(TARGET_CHANNEL, new_message)
        print("پیام با موفقیت ویرایش و فوروارد شد.")
    except Exception as e:
        print(f"خطا در ارسال پیام به کانال مقصد: {e}")

async def main():
    print("ربات فعال شد و در حال گوش دادن به کانال‌ها است...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.start()
    client.loop.run_until_complete(main())
