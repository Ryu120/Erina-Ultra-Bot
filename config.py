import os
from os import getenv

API_ID = int(getenv("API_ID",7660472))
API_HASH = getenv("API_HASH","27251e755b145296aaec806e327547d6")
TOKEN = getenv("BOT_TOKEN","5638679769:AAHOPjHsOP7mhJl2eQa-s7mLxC18SDTptDU")
MONGO_URI = getenv("MONGO_URI","mongodb+srv://erina:erina@cluster0.gjwlr.mongodb.net/cluster0?retryWrites=true&w=majority")
OWNER_ID = int(os.environ.get("OWNER_ID", "7351948"))
OWNER_ID2 = int(os.environ.get("OWNER_ID", "7351948"))
