from telegram import ForceReply, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

import requests
from requests.auth import HTTPBasicAuth

import daisySecrets


async def train_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_args = update.message.text.split(' ')

    origin = message_args[1].upper()
    destination = message_args[2].upper()

    url = f"https://api.rtt.io/api/v1/json/search/{origin}/to/{destination}"
    response = requests.get(url, auth=HTTPBasicAuth(
        daisySecrets.rttuser, daisySecrets.rttpass))
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

    for service in services[:5]:
        time = service['locationDetail']['gbttBookedDeparture']
        operator = service['atocCode']
        dest = service['locationDetail']["destination"][0]['description']
        
        try:
            if service["serviceType"] == "train":
                platform = "Plt " + service['locationDetail']["platform"]

                if len(platform) == 5:
                    platform += " "
                
                try:
                    if service['locationDetail']["serviceLocation"] == "AT_PLAT":
                        platform += " (at)"
                    elif service['locationDetail']["serviceLocation"] == "APPR_PLAT":
                        platform += " (appr)"
                    elif service['locationDetail']["serviceLocation"] == "APPR_STAT":
                        platform += " (appr)"
                    elif service['locationDetail']["serviceLocation"] == "DEP_PREP":
                        platform += " (dep)"
                    elif service['locationDetail']["serviceLocation"] == "DEP_READY":
                        platform += " (dep)"
                    else:
                        platform += " (" + service['locationDetail']["serviceLocation"] + ")"
                except:
                    if service['locationDetail']['platformConfirmed']:
                        platform += " (conf)"
                    else:
                        platform += " (ind)"

            elif service["serviceType"] == "bus":
                platform = "Bus"
            elif service["serviceType"] == "ship":
                platform = "Ship"
            else:
                platform = "Plt UNK"

            print(platform)
        
        except:
            print('failed to find platform')
            platform = "Plt UNK"
            print(platform)
        
        for i in range(13 - len(platform)):
            platform += " "

        replyText = replyText + "\n" + f"`{time} {platform} [{operator}] {dest}`"

    await update.message.reply_text(replyText, parse_mode=ParseMode.MARKDOWN)
