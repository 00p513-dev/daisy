#!/usr/bin/env python

import logging
import random
from typing import Optional

import daisySecrets
from telegram import Update, User
from telegram.ext import Application, CommandHandler, ContextTypes

import rtt
import tfl

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user: Optional[User] = update.effective_user
    greetings = ["Hewwo", "Haiii", "OwO It's an", "meow meow"]

    if user is not None and update.message is not None:
        await update.message.reply_html(
            # this isn't a cryptographic function
            rf"{random.choice(greetings)} {user.mention_html()}!"  # nosec
        )


async def strike_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a list of strikes. Get Amy to update it because there isn't a strike api
    anywhere"""
    if update.message is not None:
        await update.message.reply_html(
            """<b>18th March</b> - RMT TOCs
<b>30th March</b> - RMT TOCs
<b>1st April</b> - RMT TOCs"""
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    if update.message is not None:
        await update.message.reply_html(
            """
OwO henwo! This is a Tewegwam bot Amewia has been wowking on.

<b>Commands:</b>
/tflbus - Gives the status of a given TfL route


/tflstatus - Gives the status of a specified TfL rail route. If none specified, displays all TfL lines.


/trains - Gives the next trains between two mainline stations.


/strikes - Gives a list of upcoming strikes. May be inaccurate as Amelia has to update it from time to time (its cursed).
""")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(daisySecrets.bot_token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("strikes", strike_command))
    application.add_handler(CommandHandler("tflstatus", tfl.tflstatus_command))
    application.add_handler(CommandHandler("tflbus", tfl.tflbus_command))
    application.add_handler(CommandHandler("train", rtt.train_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
