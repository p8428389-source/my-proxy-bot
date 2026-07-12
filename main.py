import os
import re
import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest

# --- اطلاعات اکانت، کانال و گروه‌ها ---
API_ID = 38386228
API_HASH = '4e787e48c8b9faf1dd2f44249c64c841'
SOURCE_CHANNEL = '@filembad'
TARGET_CHANNEL = '@npv_proxy7'
BOT_USERNAME = '@npv_proxy7_bot'

TARGET_GROUPS = ['@TablightAzad9', '@Sama_forsin']
FORCED_CHANNELS = []

CHECK_DELAY = 120
MAX_WARNINGS = 3
NEW_NAME = '%40npv_proxy7'
# ------------------------------------------------

client = TelegramClient('session_userbot', API_ID, API_HASH)
group_warnings = {group: 0 for group in TARGET_GROUPS}

V2RAY_PREFIXES = ('vless://', 'vmess://', 'ss://', 'trojan://', 'tg://')
TG_PROXY_PREFIXES = ('t.me/proxy?', 'tg://proxy?')

CUSTOM_CAPTION = (
    "وصل بشی جوین ندی حرومه😂\n"
    "[https://t.me/npv_proxy7](https://t.me/npv_proxy7)\n"
    "[https://t.me/npv_proxy7](https://t.me/npv_proxy7)\n"
    "[https://t.me/npv_proxy7](https://t.me/npv_proxy7)"
)

async def check_and_join_forced_channels():
    for channel in FORCED_CHANNELS:
        try: 
            await client(JoinChannelRequest(channel))
        except: 
            pass

def clean_v2ray_configs(text, new_name):
    lines = text.split('\n')
    valid_configs = []
    for line in lines:
        line = line.strip()
        if any(p in line for p in V2RAY_PREFIXES):
            for p in V2RAY_PREFIXES:
                if p in line:
                    line = line[line.find(p):]
                    break
            if '#' in line: 
                line = line.split('#')[0]
            elif '%40' in line: 
                line = line.split('%40')[0]

            line = f"{line}#{new_name}"
            valid_configs.append(line)
    return '\n\n'.join(valid_configs)

def extract_tg_proxies(text):
    lines = text.split('\n')
    proxies = []
    for line in lines:
        line = line.strip()
        if any(p in line for p in TG_PROXY_PREFIXES):
            proxies.append(line)
    return proxies

def clean_filename(filename, ext):
    base_name = filename[:-len(ext)] if filename.endswith(ext) else filename
    return base_name

# برای اجرای اولیه و ثبت سشن
async def main():
    print("Userbot is starting...")
    await check_and_join_forced_channels()
    print("Logged in successfully!")

with client:
    client.loop.run_until_complete(main())
