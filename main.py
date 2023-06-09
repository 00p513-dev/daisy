#!/usr/bin/env python

import logging
import random

import daisySecrets
from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This program is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

from telegram import ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters

import davwheat, lineageos, pizza, rtt, tfl, updater

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    greetings = ["Hewwo", "Haiii", "OwO It's an", "meow meow"]
    await update.message.reply_html(
        rf"{random.choice(greetings)} {user.mention_html()}!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_html(
        """
OwO henwo! This is a Tewegwam bot Amewia has been wowking on.

<b>Commands:</b>
/codename - Gives the name of a device, when given its codename


/crs - Looks up a given station's CRS code.


/pizza <size> <type> - Order yourself a pizza for a given size and type.


/tflbus - Gives the next buses from a given TfL bus stop, using the 5 digit code for the SMS service.


/status - Gives the status of a specified rail route. If none specified, displays all TfL lines.


/train - Gives the next trains between two mainline stations. Use CRS codes.
""")

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    if query.data == 'confirmPizza':
        # Get the stored message ID
        message_id = context.bot_data.get(update.effective_chat.id)

        # Edit the message to indicate the order has been confirmed
        await query.message.reply_text("Your order has been delivered. Enjoy your pizza!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Leave a tip", url="https://monzo.me/memediatek")]]))
        await query.message.edit_reply_markup()

    elif query.data == 'cancelPizza':
        await query.message.reply_text("I agree, that was a terrible idea. Your order has been cancelled.")
        await query.message.edit_reply_markup()

    # Answer the callback query to remove the "Pending" status
    await query.answer()

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(daisySecrets.bot_token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("crs", davwheat.crs_command))
    application.add_handler(CommandHandler("codename", lineageos.codename_command))
    application.add_handler(CommandHandler("pizza", pizza.pizza_command))
    application.add_handler(CommandHandler("train", rtt.train_command))
    application.add_handler(CommandHandler("tflstatus", tfl.tflstatus_command))
    application.add_handler(CommandHandler("status", tfl.tflstatus_command))
    application.add_handler(CommandHandler("tflbus", tfl.tflbus_command))
    application.add_handler(CommandHandler("update", updater.update_command))

    application.add_handler(CallbackQueryHandler(handle_callback_query))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
