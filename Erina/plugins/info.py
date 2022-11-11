from Erina import bot, OWNER_ID, OWNER_ID2
from pyrogram import filters
from ..utils.func import *
import os
import asyncio

def parse_com(com, key):
  try:
    r = com.split(key,1)[1]
  except KeyError:
    return None
  r = (r.split(" ", 1)[1] if len(r.split()) >= 1 else None)
  return r

@bot.on_message(filters.command("info"))
async def info(bot, message):
  if message.reply_to_message:
    user = message.reply_to_message.from_user.id
  else:
    com = parse_com(message.text, "info")
    if com:
      user = com.split()[0]
      if user.isdigit():
        user = int(user)
      else:
        user = user.replace("@","")
    else:
      user = message.from_user.id
  dta = await bot.get_users(user)
  data = f"""

**|-First Name** : {dta.first_name}
**|-Last Name**: {dta.last_name}
**|-ID:** {dta.id}
**|-DC:** {dta.dc_id}
**|-Username:** @{dta.username}
**|-PermaLink**: {dta.mention}

**|-EMPEROR:** {dta.id in OWNER_ID}
**|-MONARCH:** {dta.id in OWNER_ID2}
"""
  if is_gban:
    data += f"\n\n**|-Gban Reason**: {is_gban['reason']}"
  if dta.photo:
    pic = await bot.download_media(dta.photo.big_file_id)
    kk = await message.reply_text(text="`Analyzing The User`")
    await asyncio.sleep(2)
    mm = await kk.edit_text("`...`")
    await asyncio.sleep(2)
    ll = await mm.edit_text("`Processing...`")
    await asyncio.sleep(3)
    await ll.delete()
    await message.reply_photo(photo=pic, caption=data)
    os.remove(pic)
  else:
    await message.reply_text(data, disable_web_page_preview=True)
  

  
  
@bot.on_message(filters.command('id'))
async def ids(_,message):
  if message.reply_to_message:
    user = message.reply_to_message.from_user.id
  else:
    com = parse_com(message.text, "id")
    if com:
      user = com.split()[0]
      if user.isdigit():
        user = int(user)
      else:
        user = user.replace("@","")
    else:
      user = None
  if user:
    reply = await bot.get_users(user)
    await message.reply_text(f"**Your ID**: `{message.from_user.id}`\n**{reply.first_name}'s ID**: `{reply.id}`\n**{message.chat.title}'s ID**: `{message.chat.id}`")
  else:
    await message.reply(f"**Your ID**: `{message.from_user.id}`\n**{message.chat.title}'s ID**: `{message.chat.id}`")


@bot.on_message(filters.command("mediaid"))
async def _mediaid(_, message):
  m = message.reply_to_message
  if not m:
    await message.reply_text("`Reply To Some Media`")
  else:
    if not m.media:
      await message.reply_text(f"**Message Type**: `Text`\n**Message ID**: `{m.message_id}`")
    else:
      if m.sticker:
        mfile = m.sticker.file_id
      if m.photo:
        mfile = m.photo.file_id
      if m.audio:
        mfile = m.audio.file_id
      if m.video:
        mfile = m.video.file_id
      if m.document:
        mfile = m.document.file_id
      if m.animation:
        mfile = m.animation.file_id
      await message.reply_text(f"**Message Type**: `{m.media}`\n**Message ID**: `{mfile}`")


__MODULE__ = "INFO"
__HELP__ = """
× info [reply to message | username | id] - Get Info of User
× id [reply to message | username | id] - Get ID 
× mediaid [reply to message] - Get file id
"""
