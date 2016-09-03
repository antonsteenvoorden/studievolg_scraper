from telegram.ext import Updater, CommandHandler
import sys, os, json, logging, requests, pickle
import itertools


class Notifier(Updater):
    config = None
    notifier = None
    scraper = None
    token = None
    request_url = None
    dispatcher = None
    message_text = None
    chat_id = None
    file_path = os.path.dirname(os.path.realpath(__file__))
    temporary_save = file_path + '/cijfers'
    old_cijfers = None

    def __init__(self, config, scraper):
        self.config = config
        self.scraper = scraper
        self.token = config['telegram_token']
        self.request_url = 'https://api.telegram.org/bot%s/' % self.token
        self.notifier = Updater(token=self.token)
        self.message_text = config['message']
        self.dispatcher = self.notifier.dispatcher

        cijfers_handler = CommandHandler('cijfers', self.send_cijfers)
        self.dispatcher.add_handler(cijfers_handler)
        self.notifier.start_polling()

    def check_if_new(self, new_cijfers):
        difference = None
        print('got cijfers', len(new_cijfers))
        self.old_cijfers = self.get_saved_cijfers()

        if not self.old_cijfers:
            self.write_tmp_cijfers(new_cijfers)
            self.send_update_message(new_cijfers)
            return False

        difference = self.check_diff(self.old_cijfers, new_cijfers)

        if not difference:
            return False

        print('Going to use the differences?')
        self.send_update_message(difference)

    def check_diff(self, oud, nieuw):
        difference = list(itertools.ifilterfalse(lambda x: x in oud, nieuw))\
                     + list(itertools.ifilterfalse(lambda x: x in nieuw, oud))
        print('differences: ', difference)
        if len(difference) == 0:
            # return [{"Text": "Geen verschil jonge"}]
            return False

        return difference

    def write_tmp_cijfers(self, cijfers):
        with open(self.temporary_save, 'w') as data_file:
            json.dump(cijfers, data_file)
            data_file.close()

    def send_cijfers(self, bot, update):
        if self.config['chat_id'] == '':
            self.config['chat_id'] = update.message.chat_id
            self.chat_id = self.config['chat_id']

            print('first time using the chat id, writing to config file..')

            file = open(self.file_path + '/config.json', 'w')
            file.write(json.dumps(self.config))
            file.close()

        new_cijfers = self.scraper.get_cijferlijst()
        if len(new_cijfers) == 0:
            new_cijfers = self.get_saved_cijfers()
        # text_to_send = self.format_text(new_cijfers)

        bot.sendMessage(chat_id=update.message.chat_id, text=self.message_text + json.dumps(new_cijfers, indent=2, sort_keys=True))

    def get_saved_cijfers(self):
        # bestaat cijfers file? anders aanmaken
        if not os.path.isfile(self.temporary_save):
            return False

        with open(self.temporary_save, 'r') as data_file:
            self.old_cijfers = json.load(data_file)
            return self.old_cijfers

    def send_update_message(self, cijfer_list):
        self.chat_id = self.config['chat_id']
        if self.chat_id != '':
            # text_to_send = self.format_text(cijfer_list)
            print('going to send this list:', cijfer_list)
            re = requests.post(url=self.request_url + 'sendMessage',
                               data={
                                   'chat_id': self.chat_id,
                                   'text': self.message_text + json.dumps(cijfer_list, indent=2, sort_keys=True)
                               })
        else:
            print('Geen chat_id gevonden, zorg dat je minstens 1x /cijfers tegen de bot gezegd hebt!')

    def format_text(self, cijfer_list):
        new_text = ''
        for list in cijfer_list:
            print('list is', list)
            text_to_append = ''
            for element in list:
                text_to_append += element+'\n'
            new_text += text_to_append + '\n'
        return new_text
