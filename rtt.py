"""Fetch information about current trains from realtimetrains.com"""
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

import requests
from requests.auth import HTTPBasicAuth

import daisySecrets


async def train_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return

    message_args = update.message.text.split(' ')

    origin = message_args[1].upper()
    destination = message_args[2].upper()

    url = f"https://api.rtt.io/api/v1/json/search/{origin}/to/{destination}"
    response = requests.get(url, auth=HTTPBasicAuth(daisySecrets.rttuser, daisySecrets.rttpass))
    data = response.json()

    try:
        services = data['services']
    except:
        await update.message.reply_text("Something went wrong, you probably have requested a non-existent station")
        return
    
    if not services:
        await update.message.reply_text("No trains available.")
        return

    replyText = ""

    for service in services[:3]:
        time = service['locationDetail']['gbttBookedDeparture']
        operator = service['atocCode']
        dest = service['locationDetail']["destination"][0]['description']
        replyText = replyText + "\n" + f"{time} [{operator}] {dest}"

    await update.message.reply_text(replyText)
