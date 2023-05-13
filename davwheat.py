from telegram import ForceReply, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

import requests
from requests.auth import HTTPBasicAuth

import daisySecrets

async def crs_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Looks up a CRS code for a requested train station using David Wheatley's API"""

    message_args = update.message.text.split(' ')

    search_term = ""
    
    for i in message_args[1:]:
        if len(search_term) >= 1:
            search_term += " "
        search_term += i

    url = f"https://national-rail-api.davwheat.dev/crs/{search_term}"

    response = requests.get(url)

    if response.status_code != 200: 
        await update.message.reply_text(f"The request failed: \n{response.raw}", parse_mode=ParseMode.MARKDOWN)
        return
    
    data = response.json()

    if len(data) == 0:
        await update.message.reply_text(f"No stations found.", parse_mode=ParseMode.MARKDOWN)
        return

    # If we made it this far chances are there are some stations to be found :)

    replyText = ""

    for station in data:
        replyText += "\n" + f"`{station['crsCode']}: {station['stationName']}`"

    await update.message.reply_text(replyText, parse_mode=ParseMode.MARKDOWN)