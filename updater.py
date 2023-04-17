from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

import git

import daisySecrets


async def update_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_args = update.message.text.split(' ')

    if update.message.from_user.id not in daisySecrets.admin_users:
        await update.message.reply_text("You aren't able to do that...")
        return
    
    # Open the Git repository in the current working directory
    repo = git.Repo()

    # Get the local and remote references
    local_ref = repo.head.commit
    remote_ref = repo.remotes.origin.refs.main.commit

    # Fetch the latest changes from the remote repository
    await update.message.reply_text("Checking for updates...")
    repo.remotes.origin.fetch()

    # Check if the local and remote references are the same
    if local_ref == remote_ref:
        await update.message.reply_text("The bot is up to date.")
    else:
        await update.message.reply_text("Updating...")
        repo.git.pull()
        await update.message.reply_text("Updated!")
