from telegram import ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

async def pizza_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_args = update.message.text.split(' ')

    try:
        pizzaSize = int(message_args[1])
        pizzaType = message_args[2]

        try:
            for i in message_args[3:]:
                pizzaType += " " + i
        except:
            pass

        pizzaPrice = (pizzaSize * 1.5) + 4
        pizzaPrice = format(pizzaPrice,'.2f')

        # Create the order message
        order_message = f"Your order:\nPizza: {pizzaType}\nSize: {pizzaSize}\nPrice: ${pizzaPrice}"

        # Create inline keyboard buttons
        confirm_button = InlineKeyboardButton("I want it!", callback_data="confirmPizza")
        cancel_button = InlineKeyboardButton("Never mind thats awful", callback_data="cancelPizza")

        # Create inline keyboard markup
        reply_markup = InlineKeyboardMarkup([[confirm_button, cancel_button]])

        # Send the order message with the inline keyboard
        await update.message.reply_text(order_message, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

    except (IndexError, ValueError):
        await update.message.reply_text('There are not enough arguments')
