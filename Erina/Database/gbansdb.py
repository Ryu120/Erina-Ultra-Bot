from Erina import db

async def get_gbans():
  gbans_list = []
  async for gban in db.gbans.find({"id": {"$gt": 0}}):
    gbans_list.append(gban['id'])
  return gbans_list


async def add_gban(gban: int, reason):
  gbans = await get_gbans()
  if gban in gbans:
    return
  else:
    return await db.gbans.insert_one({"id": gban, "reason": reason})


async def del_gban(gban: int):
    gbans = await get_gbans()
    if gban in gbans:
      return await db.gbans.delete_one({"id": gban})
    else:
      return


async def get_gban(gban: int):
  gban_dict = await db.gbans.find_one({"id": gban})
  if gban_dict:
    gban_dict.pop("_id")
    return gban_dict
  else:
    return None
