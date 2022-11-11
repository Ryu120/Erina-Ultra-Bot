from Erina import bot
import logging
from Erina.plugins import ALL_MODULES
from pyrogram import idle
import importlib
from pyrogram import filters
from Erina import BOT_USERNAME
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup 
import asyncio

from math import ceil

from pyrogram.types import InlineKeyboardButton

from Erina import MOD_LOAD, MOD_NOLOAD

class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text

HELPABLE = {}    
    
PM_ERINA_TEXT = """
**𝑆𝑢𝑝 !!! 𝐼 𝐴𝑚 𝐸𝑟𝑖𝑛𝑎, 𝑁𝑖𝑐𝑒 𝑇𝑜 𝑀𝑒𝑒𝑡 𝑌𝑜𝑢 !!**
𝐼 𝑎𝑚 𝐴𝑛𝑑 𝑎𝑑𝑣𝑎𝑛𝑐𝑒𝑑 𝐵𝑜𝑡
**ʀᴇᴘᴏʀᴛ ɪꜱꜱᴜᴇꜱ - @ErinaSupport**
"""

PM_ERINA_PIC = "https://telegra.ph/file/7107cb1bb3d4abc76b9c5.jpg"



START_KEYBOARD = InlineKeyboardMarkup(
  [
    [
      InlineKeyboardButton(
        text="Help",
        callback_data="bot_commands"
      ),
      InlineKeyboardButton(
        text="About Me",
        callback_data="abouterina"
      )
    ],
    [
      InlineKeyboardButton(
        text="Add To Your Group",
        url=f"https://t.me/{BOT_USERNAME}?startgroup=new"
      )
    ]
  ]
)

@bot.on_message(filters.command('start'))
async def miostart(_, message):
    return await message.reply_photo(
      photo=PM_ERINA_PIC,
      caption=PM_ERINA_TEXT,
      reply_markup=START_KEYBOARD
    ) 

def paginate_modules(page_n, module_dict, prefix, chat=None):
    if not chat:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__MODULE__,
                    callback_data="{}_module({})".format(
                        prefix, x.__MODULE__.replace(" ", "_").lower()
                    ),
                )
                for x in module_dict.values()
            ]
        )
    else:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__MODULE__,
                    callback_data="{}_module({},{})".format(
                        prefix, chat, x.__MODULE__.replace(" ", "_").lower()
                    ),
                )
                for x in module_dict.values()
            ]
        )

    pairs = list(zip(modules[::3], modules[1::3], modules[2::3]))
    i = 0
    for m in pairs:
        for _ in m:
            i += 1
    if len(modules) - i == 1:
        pairs.append((modules[-1],))
    elif len(modules) - i == 2:
        pairs.append(
            (
                modules[-2],
                modules[-1],
            )
        )

    COLUMN_SIZE = 4

    max_num_pages = ceil(len(pairs) / COLUMN_SIZE)
  


def is_module_loaded(name):
    return (not MOD_LOAD or name in MOD_LOAD) and name not in MOD_NOLOAD  
  
BOT_NAME = "Erina"  
  
async def help_parser(name, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    return (
        """Hello {first_name}, My name is Erina.
I'm a group management bot with some useful features.
You can choose an option below, by clicking a button.
Also you can ask anything in Support Group.
""".format(
            first_name=name,
            bot_name=BOT_NAME,
        ),
        keyboard,
    )
  
  
@bot.on_callback_query(filters.regex("bot_commands"))
async def commands_callbacc(_, CallbackQuery):
    text, keyboard = await help_parser(CallbackQuery.from_user.mention)
    await bot.send_message(
        CallbackQuery.message.chat.id,
        text=text,
        reply_markup=keyboard,
    )

    await CallbackQuery.message.delete()
  
  
FORMAT = "[INFO] %(message)s"

if __name__ == "__main__":
    logging.basicConfig(
        handlers=[logging.FileHandler("logs.txt"), logging.StreamHandler()],
        level=logging.INFO,
        format=FORMAT,
        datefmt="[%X]",
    )
    logging.getLogger("pyrogram").setLevel(logging.INFO)
    for module in ALL_MODULES:
      importlib.import_module("Erina.plugins." + module)
    
    print("I AM NOW ONLINE") 
    print("Project By Ryu120, Gift to my bich Tarun")
    idle()
    with bot:
        bot.send_message(-1001870797355 , "I Am Now online")
