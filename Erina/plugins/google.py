import os
import re
import urllib
import urllib.parse
import urllib.request
from urllib.error import URLError, HTTPError
import requests
from bs4 import BeautifulSoup
from pyrogram import filters
from pyrogram.types import InputMediaPhoto, Message
from inspect import getfullargspec
from random import randint
from Erina.plugins.info import parse_com
from Erina import bot

opener = urllib.request.build_opener()
useragent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.38 "
    "Safari/537.36 "
)
opener.addheaders = [("User-agent", useragent)]

def ParseSauce(googleurl):
    source = opener.open(googleurl).read()
    soup = BeautifulSoup(source, "html.parser")

    results = {"similar_images": "", "override": "", "best_guess": ""}

    try:
        for bess in soup.findAll("a", {"class": "PBorbe"}):
            url = "https://www.google.com" + bess.get("href")
            results["override"] = url
    except BaseException:
        pass

    for similar_image in soup.findAll("input", {"class": "gLFyf"}):
        url = "https://www.google.com/search?tbm=isch&q=" + urllib.parse.quote_plus(
            similar_image.get("value")
        )
        results["similar_images"] = url

    for best_guess in soup.findAll("div", attrs={"class": "r5a77d"}):
        results["best_guess"] = best_guess.get_text()

    return results

def scam(imgspage, lim):
    """Parse/Scrape the HTML code for the info we want."""

    single = opener.open(imgspage).read()
    decoded = single.decode("utf-8")
    if int(lim) > 10:
        lim = 10

    imglinks = []
    counter = 0

    pattern = r"^,\[\"(.*[.png|.jpg|.jpeg])\",[0-9]+,[0-9]+\]$"
    oboi = re.findall(pattern, decoded, re.I | re.M)

    for imglink in oboi:
        counter += 1
        imglinks.append(imglink)
        if counter >= int(lim):
            break

    return imglinks

async def eor(msg: Message, **kwargs):
    func = (
        (msg.edit_text if msg.from_user.is_self else msg.reply)
        if msg.from_user
        else msg.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})

def get_file_id_from_message(
    message,
    max_file_size=3145728,
    mime_types=["image/png", "image/jpeg"],
):
    file_id = None
    if message.document:
        if int(message.document.file_size) > max_file_size:
            return

        mime_type = message.document.mime_type

        if mime_types and mime_type not in mime_types:
            return
        file_id = message.document.file_id

    if message.sticker:
        if message.sticker.is_animated:
            if not message.sticker.thumbs:
                return
            file_id = message.sticker.thumbs[0].file_id
        else:
            file_id = message.sticker.file_id

    if message.photo:
        file_id = message.photo.file_id

    if message.animation:
        if not message.animation.thumbs:
            return
        file_id = message.animation.thumbs[0].file_id

    if message.video:
        if not message.video.thumbs:
            return
        file_id = message.video.thumbs[0].file_id
    return   
  
@bot.on_message(filters.command(["reverse", "grs", "pp"]))
async def reverse_image_search(client, message: Message):
    if not message.reply_to_message:
        return await eor(
            message, text="`Reply To A Message To Reverse Search It`"
        )
    reply = message.reply_to_message
    if (
        not reply.document
        and not reply.photo
        and not reply.sticker
        and not reply.animation
        and not reply.video
    ):
        return await eor(
            message,
            text="`Reply To An Image/Document/Sticker/Animation To Reverse Search It`",
        )
    m = await eor(message, text="`Searching...`")
    #file_id = get_file_id_from_message(reply)
    image = await message.reply_to_message.download(f"{randint(1000, 10000)}.jpg")
    try:
        searchUrl = "https://www.google.com/searchbyimage/upload"
        multipart = {
            "encoded_image": (image, open(image, "rb")),
            "image_content": "",
        }
        response = requests.post(searchUrl, files=multipart, allow_redirects=False)
        fetchUrl = response.headers["Location"]

        if response != 400:
            xx = await m.edit_text(
                "`Image Was Successfully Uploaded To Google.`\n`Parsing Source Now Maybe.`"
            )
        else:
            xx = await message.reply_text(
                "`Google Told Me To Go Away`"
            )
            return

        os.remove(image)
        match = ParseSauce(fetchUrl + "&hl=en")
        guess = match["best_guess"]
        if match["override"] and match["override"] != "":
            imgspage = match["override"]
        else:
            imgspage = match["similar_images"]

        if guess and imgspage:
            await xx.edit_text(
                f"[{guess}]({fetchUrl})\n`Looking For Images...`",
                disable_web_page_preview=True,
            )
        else:
            await xx.edit_text("`Couldn't Find Anything`")
            return

        images = scam(imgspage, 2)
        if len(images) == 0:
            await xx.edit_text(
                f"[{guess}]({fetchUrl})\n\n[Visually Similar Images]({imgspage})",
                disable_web_page_preview=True,
            )
            return

        imglinks = []
        for link in images:
            lmao = InputMediaPhoto(media=str(link))
            imglinks.append(lmao)

        await message.reply_media_group(
            media=imglinks
        )
        await xx.edit_text(
            f"[{guess}]({fetchUrl})\n\n[Visually Similar Images]({imgspage})",
            disable_web_page_preview=True,
        )

    except Exception:
        print(Exception)


__MODULE__ = "REVERSE"
__HELP__ = """
Search image

× reverse [reply to image] - get search results for an image
× grs [reply to image] - get search results for an image
× pp [reply to image] - get search results for an image

"""
