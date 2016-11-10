#!/usr/bin/python

from scrape import Scraper
from apscheduler.schedulers.blocking import BlockingScheduler
from notify import TelegramNotifier, MailNotifier
import sys, os, json, logging

config = None
notifier = None
scraper = None
file_path = os.path.dirname(os.path.realpath(__file__))

"""
@author 	Anton Steenvoorden
@contact 	antonsteenvoorden@gmail.com
@date 	    04-09-2016
@version 	1.1

Maak gebruik van de @BotFather https://core.telegram.org/bots#6-botfather
plak de token van je bot in config.json bij telegram_token
Note: Bots can't initiate conversations with users.
A user must either add them to a group or send them a message first.
People can use telegram.me/<bot_username> links or username search to find your bot.
"""

def fetch_config():
    global config
    with open(file_path+'/config.json') as data_file:
        config = json.load(data_file)
    return config

def run_scraper():
    global scraper, notifier, config

    cijfers = scraper.scrape()
    if notifier != None :
        notifier.check_if_new(cijfers)

def main():
    global scraper, notifier, config
    config = fetch_config()

    if config['logging'] == "True":
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level = logging.DEBUG)

    logger = logging.getLogger()

    scraper = Scraper(config['username'],config['password'])
    interval = config['interval']

    if config['telegram_token'] != "":
        notifier = TelegramNotifier(config, scraper)
    elif config['email_username'] != "" and config['email_password'] != "":
        notifier = MailNotifier(config, scraper)

    scheduler = BlockingScheduler(standalone=True)
    scheduler.add_job(run_scraper, 'interval', minutes=interval)

    try:
        logger.info('starting schedular')
        scheduler.start()
    except (KeyboardInterrupt):
        print('Caught interrupt, stopping!')
        scheduler.shutdown(wait=False)
        os._exit(1)
        sys.exit(0)

if __name__ == "__main__":
    main()
