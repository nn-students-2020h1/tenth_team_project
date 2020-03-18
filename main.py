# coding=utf8
import os
import logging
import requests
import json

from telegram import Bot, Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater

import settings


# if __name__ == '__main__':
#     print(os.getenv("TG_TOKEN"))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def most_popular_fact(update: Update, context: CallbackContext):
    best_fact = None
    r = requests.get("https://cat-fact.herokuapp.com/facts")
    for fact in r.json()["all"]:
        best_fact = fact if best_fact is None else best_fact
        if fact["upvotes"] > best_fact["upvotes"]:
            best_fact = fact
    update.message.reply_text(f'The most popular fact is: {best_fact["text"]}')

def authors(update: Update, context: CallbackContext):
    response = requests.get("https://cat-fact.herokuapp.com/facts")
    authors = [fact["user"] for fact in response. json()["all"] if "user" in fact]
    board = dict()
    for author in authors:
        _id = author["_id"]
        board.setdefault(_id, 0)
        board[_id] += 1
    board = tuple(board.items())
    board = sorted(board, key=lambda author: author[1], reverse=True)
    author1 = list(filter(lambda author: author["_id"] == board[0][0], authors))[0]
    author2 = list(filter(lambda author: author["_id"] == board[1][0], authors))[0]
    author3 = list(filter(lambda author: author["_id"] == board[2][0], authors))[0]
    update.message.reply_text(
        f"The most popular authors are: \n\n"
        f"#1 {author1['name']['first']} {author1['name']['last']} \nNumber of posts: {board[0][1]}\n"
        f"#2 {author2['name']['first']} {author2['name']['last']} \nNumber of posts: {board[1][1]}\n"
        f"#3 {author3['name']['first']} {author3['name']['last']} \nNumber of posts: {board[2][1]}\n"
    )

def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    update.message.reply_text(f'Привет, {update.effective_user.first_name}!')


def chat_help(update: Update, context: CallbackContext):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Введи команду /start для начала. ')


def echo(update: Update, context: CallbackContext):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


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
    updater.dispatcher.add_handler(CommandHandler('authors', authors))
    updater.dispatcher.add_handler(CommandHandler('fact', most_popular_fact))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', chat_help))

    # on noncommand i.e message - echo the message on Telegram
    updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    logger.info('Start Bot')
    main()
