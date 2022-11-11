import asyncio

from pyrogram import filters , Client
from motor.motor_asyncio import AsyncIOMotorClient as async_mongo
from typing import Union
import os 
import time
from config import *
from telegram.ext import Application, Defaults

bot = Client(
    'Erina',
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN
)

print("[INFO]: INITIALIZING DATABASE")
async_mongo_client = async_mongo(MONGO_URI)
db = async_mongo_client.erina

ENV = bool(os.environ.get("ENV", False))

if ENV:
    TOKEN = os.environ.get("TOKEN")

    try:
        OWNER_ID = int(os.environ.get("OWNER_ID"))
    except ValueError:
        raise Exception("Your OWNER_ID is wrong bruh.")
    
    try:
        OWNER_ID2 = int(os.environ.get("OWNER_ID2"))
    except ValueError:
        raise Exception("Your OWNER_ID2 is wrong bruh.")



START_TIME = time.time()
bot.start()
x = bot.get_me()
BOT_USERNAME = x.username
BOT_NAME = x.first_name
BOT_ID = x.id 

x = None

PTB = Application.builder().token(TOKEN).build()
asyncio.get_event_loop().run_until_complete(PTB.bot.initialize())



MOD_LOAD = []
MOD_NOLOAD = []
