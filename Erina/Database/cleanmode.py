#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
# Copyright (C) 2022-2023 by theblacklinen@Github, < https://github.com/theblacklinen >.

# This file is part of < https://github.com/theblacklinen/Erina-Ultra-Bot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/theblacklinen/Erina-Ultra-Bot/blob/master/LICENSE >
#
# All rights reserved.
#


from Erina import db

cleandb = db.cleanmode
cleanmode = {}


async def is_cleanmode_on(chat_id: int) -> bool:
    mode = cleanmode.get(chat_id)
    if not mode:
        user = await cleandb.find_one({"chat_id": chat_id})
        if not user:
            cleanmode[chat_id] = True
            return True
        cleanmode[chat_id] = False
        return False
    return mode


async def cleanmode_on(chat_id: int):
    cleanmode[chat_id] = True
    user = await cleandb.find_one({"chat_id": chat_id})
    if user:
        return await cleandb.delete_one({"chat_id": chat_id})


async def cleanmode_off(chat_id: int):
    cleanmode[chat_id] = False
    user = await cleandb.find_one({"chat_id": chat_id})
    if not user:
        return await cleandb.insert_one({"chat_id": chat_id})
