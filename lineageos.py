from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

import requests

LINEAGEOS_ENDPOINT = 'https://download.lineageos.org/api/v2/'

def getDeviceInfo(codename, endpoint=LINEAGEOS_ENDPOINT):
    response = requests.get(endpoint + f'devices/{codename}')

    if response.status_code == 400:
        return 400
    elif response.status_code != 200:
        return 404

    data = response.json()
    return data

async def codename_command(update: Update, context: ContextTypes.DEFAULT_TYPE, endpoint=LINEAGEOS_ENDPOINT) -> None:
    message_args = update.message.text.split(' ')

    codename = message_args[1]

    data = getDeviceInfo(codename, endpoint)

    if data == 400:
        await update.message.reply_text(f"The device with codename '{codename}' is not supported by LineageOS.")
        return
    elif data == 404:
        await update.message.reply_text(f"Something went wrong.")
        return
    else:
        device_name = data['name']
        device_oem = data['oem']

    await update.message.reply_text(f"{device_oem} {device_name}")

async def lineage_command(update: Update, context: ContextTypes.DEFAULT_TYPE, endpoint=LINEAGEOS_ENDPOINT) -> None:
    message_args = update.message.text.split(' ')

    codename = message_args[1]

    data = getDeviceInfo(codename, endpoint)

    if data == 400:
        await update.message.reply_text(f"The device with codename '{codename}' is not supported by LineageOS.")
        return
    elif data == 404:
        await update.message.reply_text(f"Something went wrong.")
        return
    
    await update.message.reply_text(
        f"""
Manufacture: {data['oem']}
Device: {data['name']}
Supported Versions: {', '.join(data['versions'])}
More information: {data['info_url']}
        """)