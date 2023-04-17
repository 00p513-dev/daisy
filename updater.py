from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

import git

import daisySecrets


async def update_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_args = update.message.text.split(' ')

    # Open the Git repository in the current working directory
    repo = git.Repo()

    # Get the local and remote references
    local_ref = repo.head.commit
    remote_ref = repo.remotes.origin.refs.main

    # Fetch the latest changes from the remote repository
    repo.remotes.origin.fetch()

    # Check if the local and remote references are the same
    if local_ref == remote_ref:
        replyText = "The local repository is up-to-date."
    else:
        replyText = "Updating..."
        repo.remotes.origin.pull()
        replyText = "Updating..."

    await update.message.reply_text(replyText)
