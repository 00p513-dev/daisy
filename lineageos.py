from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

import requests

LINEAGEOS_ENDPOINT = 'https://download.lineageos.org/api/v2/'

async def codename_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_args = update.message.text.split(' ')

    codename = message_args[1]
    response = requests.get(LINEAGEOS_ENDPOINT + f'devices/{codename}')

    if response.status_code == 404:
        await update.message.reply_text(f"The device with codename '{codename}' is not supported by LineageOS.")
        return

    data = response.json()
    device_name = data['name']
    device_oem = data['oem']

    await update.message.reply_text(f"{device_oem} {device_name}")