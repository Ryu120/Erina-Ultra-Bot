import pymongo
from Erina import MONGO_URI as db_url, bot
from pyrogram import filters
from datetime import datetime, date, time 
import re
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Erina.helper_functions.cust_p_filters import admin_fliter

BTN_URL_REGEX = re.compile(r"(\[([^\[]+?)]\(buttonurl:/{0,2}(.+?)(:same)?\))")

OWNER_ID = [5553411428]
OWNER_ID2 = [5544740697]

welcome_db = pymongo.MongoClient(db_url).erina.welcome

def get_keyboard(data):
  if len([match for match in BTN_URL_REGEX.finditer(data)]) == 0:
    return data, None
  else:
    cont = data.split([match for match in BTN_URL_REGEX.finditer(data)][0].group(1), 1)[0]
    if [match for match in BTN_URL_REGEX.finditer(data)][0].group(1) in cont:
      cont = None
    lis = []
    for match in BTN_URL_REGEX.finditer(data):
      but = []
      if bool(match.group(4)):
        lis[-1].append(InlineKeyboardButton(text=match.group(2), url=match.group(3)))
      else:
        but.append(InlineKeyboardButton(text=match.group(2), url=match.group(3)))
      if len(but) != 0:
        lis.append(but)
    if len(lis) != 0:
      return cont, InlineKeyboardMarkup(lis)
    else:
      return cont, None

def parse_com(com, key):
  try:
    r = com.split(key,1)[1]
  except KeyError:
    return None
  r = (r.split(" ", 1)[1] if len(r.split()) >= 1 else None)
  return r


@bot.on_message(filters.command('setwelcome') & admin_fliter)
async def setwelcome(_,message):
    if message.text:
      welcome = parse_com(message.text, 'setwelcome')
    elif message.caption:
      welcome = parse_com(message.caption, 'setwelcome')
    else:
      welcome = None
    if not (welcome or message.reply_to_message):
      return await message.reply("Either reply to a message or give something")
    if message.reply_to_message:
      m = message.reply_to_message
      di = {}
      di['chat'] = message.chat.id
      di['media'] = m.media
      if m.media:
        di['text'] = m.caption
        if m.photo:
          di['file'] = m.photo.file_id
        elif m.video:
          di['file'] = m.video.file_id
        elif m.document:
          di['file'] = m.document.file_id
        elif m.animation:
          di['file'] = m.animation.file_id
        elif m.audio:
          di['file'] = m.audio.file_id
      else:
        di['text'] = m.text
        di['file'] = None
    else:
      di = {}
      di['chat'] = message.chat.id
      di['media'] = message.media
      if message.media:
        di['text'] = welcome
        if m.photo:
          di['file'] = message.photo.file_id
        elif m.video:
          di['file'] = message.video.file_id
        elif m.document:
          di['file'] = message.document.file_id
        elif m.animation:
          di['file'] = message.animation.file_id
        elif m.audio:
          di['file'] = message.audio.file_id
      else:
        di['text'] = welcome
        di['file'] = None
    if welcome_db.find_one({"chat": message.chat.id}):
      welcome_db.update_one({"chat": message.chat.id}, {"$set": di})
    else:
      di['welcome_on'] = True
      welcome_db.insert_one(di)
    return await message.reply("Successfully Set Welcome")
    


@bot.on_message(filters.command("clearwelcome"))
def clearwelcome(_,message):
  admins = bot.get_chat_members(message.chat.id, filter="administrators")
  if not message.from_user.id in (admins + OWNER_ID + OWNER_ID2):
    return message.reply_text("Become an admin first lol")
  else:
    welcome_db.delete_one({"chat": message.chat.id})
    return message.reply("Successfully Cleared Welcome")
  
 

@bot.on_message(filters.new_chat_members)
async def welcome(_,message):
  welcome_msg = welcome_db.find_one({"chat" : message.chat.id})
  for muser in message.new_chat_members:
    if not welcome_msg:
      await message.reply("Hello!! sup?")
    else:
      if not welcome_msg['media']:
        if welcome_msg['text']:
          cap, keyb = get_keyboard(welcome_msg['text'])
          cap = cap.format(username="@" + muser.username, mention=f"[{muser.first_name}](tg://user?id={muser.id})", chatname=message.chat.title, firstname=muser.first_name, lastname = muser.last_name, fullname=muser.first_name + (muser.last_name or ""), date=date.today(), time=f"{(datetime.today()).time()}"[:8])
          return await message.reply_text(text=cap, reply_markup=keyb)
        else:
          return await message.reply_text("Hello! sup?")
      else:
        if welcome_msg['welcome_on']:
          media = welcome_msg['media']
          file = welcome_msg['file']
          if media == 'photo':
            func = message.reply_photo
          elif media == 'video':
            func = message.reply_video
          elif media == 'audio':
            func = message.reply_audio
          elif media == 'animation':
            func = message.reply_animation
          elif media == 'document':
            func = message.reply_document
          else:
            func = None
          if welcome_msg['text']:
            cap, keyb = get_keyboard(welcome_msg['text'])
            cap = cap.format(username="@" + muser.username, mention=f"[{muser.first_name}](tg://user?id={muser.id})", chatname=message.chat.title, firstname=muser.first_name, lastname = muser.last_name, fullname=muser.first_name + (muser.last_name or ""), date=date.today(), time=f"{(datetime.today()).time()}"[:8])
          else:
            cap = None
            keyb = None
          if not func and not cap:
            return await message.reply("Hello! sup?")
          if func:
            return await func(file, caption=cap, reply_markup=keyb)


@bot.on_message(filters.command('welcome'))
async def save_get_welcome(_, message):
  q = parse_com(message.text, 'welcome')
  if not q:
    welcome_msg = welcome_db.find_one({"chat" : message.chat.id})
    if not welcome_msg:
      await message.reply("Hello!! sup?")
    else:
      if not welcome_msg['media']:
        if welcome_msg['text'] :
          cap, keyb = get_keyboard(welcome_msg['text'])
          return await message.reply_text(text=cap, reply_markup=keyb)
        else:
          return await message.reply_text("Hello! sup?")
      else:
        media = welcome_msg['media']
        file = welcome_msg['file']
        if media == 'photo':
          func = message.reply_photo
        elif media == 'video':
          func = message.reply_video
        elif media == 'audio':
          func = message.reply_audio
        elif media == 'animation':
          func = message.reply_animation
        elif media == 'document':
          func = message.reply_document
        else:
          func = None
      if welcome_msg['text']:
        cap, keyb = get_keyboard(welcome_msg['text'])
      else:
        cap = None
        keyb = None
      if not func and not cap:
        return await message.reply("Hello! sup?")
      if func:
        return await func(file, caption=cap, reply_markup=keyb)
  else:
    dk = {}
    if q.lower() in ("on", "yes"):
      dk['welcome_on'] = True
    elif q.lower() in ("off","no"):
      dk['welcome_on'] = False
    welcome_db.update_one({"chat": message.chat.id},{"$set": dk})
    return await message.reply_text(f"Successfully Changed Send Welcome To :- {'Send' if dk['welcome_on'] else 'Dont Send'}")
    
