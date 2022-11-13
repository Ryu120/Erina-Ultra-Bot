from Erina import *
from pyrogram import *
from pyrogram.types import *


@bot.on_message(filters.command("gban")& filters.group)
async def gban(_,msg:Message):
    usr = msg.reply_to_message.from_user.first_name
    await msg.reply_text(text= usr)