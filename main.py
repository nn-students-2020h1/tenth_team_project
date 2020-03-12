# coding=utf8
import os
import logging

from telegram import Bot, Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater
from datetime import datetime
import settings

# comment
# if __name__ == '__main__':
#     print(os.getenv("TG_TOKEN"))


logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def errors(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            logger = logging.getLogger()
            logger.warning(args[0] )
            logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    return inner

def my_logging(func):
    def inner(update, context):
        message = update.message
        data = {
            "func": func.__name__,

            "username": message.from_user.username,
            "first_name": message.from_user.first_name,

            "text": message.text,

            "from_id": message.from_user.id,
            "chat_id": message.chat.id,
            "language": message.from_user.language_code,
        }
        logger.debug(tuple(data.values()))
        func(update, context)

    return inner

@errors
@my_logging
def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    update.message.reply_text(f'Привет, {update.effective_user.first_name}!')
@errors
@my_logging
def chat_help(update: Update, context: CallbackContext):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Введи команду /start для начала. ')

@my_logging
def echo(update: Update, context: CallbackContext):
    """Echo the user message."""
    update.message.reply_text(update.message.text)
@errors
@my_logging
def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning(f'Update {update} caused error {context.error}')


def main():
    bot = Bot(
        token=os.getenv("TG_TOKEN"),
        base_url=os.getenv("TG_PROXY")
    )
    updater = Updater(bot=bot, use_context=True)

    # on different commands - answer in Telegram
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', chat_help))

    # on noncommand i.e message - echo the message on Telegram
    updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    updater.dispatcher.add_error_handler(error)

    logger.info('Start Bot')
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
