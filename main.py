from telethon import TelegramClient, events
from telethon.sessions import StringSession
import asyncio

api_id = 37503262
api_hash = "0fcc6deeff5e2049e6e6e47cbb282d39"

session = "1BVtsOIsBu8CTIIAnCAfQl5zqBhu1FlKpuJsKVAGxbmKX8o2xcb5P42bY1-nTprwZHLrCh0UzvfV26A-yXNg7fg7GqDT838DtnUms-mPwkL70FILhOqaPf2ycKm5C6i4Dg9RxS6aQBqA3pruvJybfb7nnX7b5pAQIVsKKHRdRxUjrswOu6ECRcpSGCbLpxl64LRWzjk2csqDy-t2ozYX5Pi-3SUvSdlrMu3w_tquGbylySvQ0AaUevcHIiySnpUFCgm4ZCNadgyUEv5vTucHIQpibXP-jXTIHM5vRG7Y6rTY_gTO0Au22zalGrS8LSWDlUdoBwO5xMdnJ9l5ICABXz9MkSzpWdsg="

client = TelegramClient(StringSession(session), api_id, api_hash)

muted_users = set()
auto_replies = {}
blash_active = {}

# ping
@client.on(events.NewMessage(pattern="ping"))
async def ping(event):
    await event.reply("pong 🔥")

# هلا
@client.on(events.NewMessage(pattern="هلا"))
async def hello(event):
    await event.reply("هلا فيك 😎")

# إضافة رد تلقائي
@client.on(events.NewMessage(pattern=r"اضف رد (.+) (.+)"))
async def add_reply(event):
    key = event.pattern_match.group(1)
    value = event.pattern_match.group(2)
    auto_replies[key] = value
    await event.reply("تم إضافة الرد")

# حذف رد
@client.on(events.NewMessage(pattern=r"حذف رد (.+)"))
async def del_reply(event):
    key = event.pattern_match.group(1)
    auto_replies.pop(key, None)
    await event.reply("تم الحذف")

# الرد التلقائي
@client.on(events.NewMessage)
async def auto_reply(event):
    if event.raw_text in auto_replies:
        await event.reply(auto_replies[event.raw_text])

# كتم
@client.on(events.NewMessage(pattern="كتم"))
async def mute(event):
    if event.is_reply:
        user = (await event.get_reply_message()).sender_id
        muted_users.add(user)
        await event.reply("تم كتمه 🔇")

# الغاء كتم
@client.on(events.NewMessage(pattern="الغاء كتم"))
async def unmute(event):
    if event.is_reply:
        user = (await event.get_reply_message()).sender_id
        muted_users.discard(user)
        await event.reply("تم فك الكتم 🔊")

# حذف رسائل (تنظيف)
@client.on(events.NewMessage(pattern="تنظيف"))
async def clear(event):
    async for msg in client.iter_messages(event.chat_id, from_user='me'):
        await msg.delete()
    await event.reply("تم تنظيف الشات 🧹")

# بلش
@client.on(events.NewMessage(pattern=r"بلش (.+)"))
async def start_blash(event):
    blash_active[event.chat_id] = event.pattern_match.group(1)
    await event.reply("تم تشغيل البلش 🔥")

@client.on(events.NewMessage(pattern="ايقاف البلش"))
async def stop_blash(event):
    blash_active.pop(event.chat_id, None)
    await event.reply("تم إيقاف البلش")

@client.on(events.NewMessage)
async def auto_blash(event):
    if event.chat_id in blash_active and not event.out:
        await event.reply(blash_active[event.chat_id])

print("السورس شغال 🔥")

client.start()
client.run_until_disconnected()
