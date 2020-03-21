# coding=utf8
#pyatkin branch
import os
import logging
import traceback
import requests
import json
from datetime import date, timedelta
import csv

from telegram import Bot, Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater

from config import msg_logs_file
import settings


logger = logging.getLogger(__name__)

def download_covid_report():
    reports_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'

    def get_response_by_date(date):
        day, month, year = date.day, date.month, date.year
        day_now = f'{month // 10}{month % 10}-{day // 10}{day % 10}-{year}'
        last_report_url = f'{reports_url}{day_now}.csv'
        return requests.get(last_report_url)

    last_date = date.today()
    r = get_response_by_date(last_date)
    while r.status_code == 404:
        last_date -= timedelta(days=1)
        r = get_response_by_date(last_date)

    with open('covid-19.csv', 'wb') as file:
        file.write(r.content)

def sort_and_rewrite_covid_report():
    with open('covid-19.csv', 'r') as file:
        reader = csv.DictReader(file)
        output_data = list(reader)
        sort_output_data = sorted(output_data, key = lambda item: (int(item['Confirmed'])
                                                                   + int(item['Deaths']) + int(item['Recovered'])), reverse=True)

    with open('covid-19-copy.csv', 'w') as handle:
        writer = csv.DictWriter(handle, fieldnames=['Province/State','Country/Region','Last Update',
                                                    'Confirmed','Deaths','Recovered','Latitude','Longitude'])
        writer.writeheader()
        for string in sort_output_data:
            writer.writerow(string)

def rewrite_covid_report_with_countries():
    with open('covid-19.csv', 'r') as file:
        reader = csv.DictReader(file)
        input_data = list(reader)

    output_data = list()
    for row in input_data:
        met = False
        for i in output_data:
            if row['Country/Region'] == i['Country/Region']:
                i['Confirmed'] = int(row['Confirmed']) + int(i['Confirmed'])
                i['Deaths'] = int(row['Deaths']) + int(i['Deaths'])
                i['Recovered'] = int(row['Recovered']) + int(i['Recovered'])
                met = True
        if met:
            continue
        out_row = {
            'Country/Region': row['Country/Region'],
            'Last Update': row['Last Update'],
            'Confirmed': row['Confirmed'],
            'Deaths': row['Deaths'],
            'Recovered': row['Recovered']
        }
        output_data.append(out_row)
    with open('covid-19.csv', 'w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=['Country/Region', 'Last Update', 'Confirmed', 'Deaths', 'Recovered'])
        writer.writeheader()
        for string in output_data:
            writer.writerow(string)

def shortMsgInfo(update):
    message = update.message
    data = {
        "username": message.from_user.username,
        "first_name": message.from_user.first_name,

        "text": message.text,

        "from_id": message.from_user.id,
        "chat_id": message.chat.id,
        "language": message.from_user.language_code,
    }
    return data


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def msg_logging(func):
    """Log Messages caused by Updates."""
    def wrapper(update, context):
        logger.debug(list(shortMsgInfo(update).values()) , extra={"func_name": func.__name__})
        func(update, context)
    return wrapper

@msg_logging
def most_popular_fact(update: Update, context: CallbackContext):
    best_fact = None
    r = requests.get("https://cat-fact.herokuapp.com/facts")
    for fact in r.json()["all"]:
        best_fact = fact if best_fact is None else best_fact
        if fact["upvotes"] > best_fact["upvotes"]:
            best_fact = fact
    update.message.reply_text(f'The most popular fact is: {best_fact["text"]}')

@msg_logging
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

@msg_logging
def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    update.message.reply_text(f'Привет, {update.effective_user.first_name}!')

@msg_logging
def chat_help(update: Update, context: CallbackContext):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Введи команду /start для начала. ')

@msg_logging
def echo(update: Update, context: CallbackContext):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

@msg_logging
def history(update: Update, context: CallbackContext):
    """Echo last 5 message from all users"""
    with open(msg_logs_file, "r", encoding='utf8') as file:
        last_5 = "".join(file.readlines()[-5:])
        update.message.reply_text(last_5)

def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning(f"{context.error}\n{traceback.format_exc()[:-1]}")

def main():
    bot = Bot(
        token=os.getenv("TG_TOKEN"),
        base_url=os.getenv("TG_PROXY")
    )
    updater = Updater(bot=bot, use_context=True, workers=-3)

    # on different commands - answer in Telegram
    updater.dispatcher.add_handler(CommandHandler('authors', authors))
    updater.dispatcher.add_handler(CommandHandler('fact', most_popular_fact))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', chat_help))
    updater.dispatcher.add_handler(CommandHandler('history', history))

    # on noncommand i.e message - echo the message on Telegram
    updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    updater.dispatcher.add_error_handler(error)

    logger.info('start bot')
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
