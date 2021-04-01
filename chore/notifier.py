import os
import subprocess

import sys

sys.path.append('/usr/src/app')

import requests
import telebot
from dotenv import load_dotenv

from chore.hooks import init_db
from chore.queries.queries import create_new_commit


load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


class Parser:

    def __init__(self):
        self.url = 'https://raw.githubusercontent.com/antonkurenkov/systembuilder_2021/develop/status.json'

    def parse(self):
        return requests.get(self.url).json()


class Notifier:

    def __init__(self, data):
        self.chat_id = 444591160  # daniil
        # self.chat_id = -414189807  # group
        self.data = list(data.values())[0]
        self.datetime = list(data.keys())[0]
        self.bot = telebot.TeleBot(TOKEN)

    @staticmethod
    def load_in_database(kwargs):
        database = init_db()
        session = database.make_session()
        create_new_commit(session=session, **kwargs)
        try:
            session.commit_session()
        except Exception as error:
            print(error)
        session.close_session()

    def prepare(self):
        data_to_load = {}
        author = subprocess.Popen(['git', 'log', '-2', '--pretty=%an'],
                                  stdout=subprocess.PIPE).communicate()[0].decode('utf-8').strip().split()[-1]
        commit_message = subprocess.Popen(['git', 'log', '-2', '--pretty=%s'],
                                          stdout=subprocess.PIPE).communicate()[0].decode('utf-8').strip(). \
            split('\n')[-1]
        commit_id = subprocess.Popen(['git', 'log', '-2', '--pretty=%h'],
                                     stdout=subprocess.PIPE).communicate()[0].decode('utf-8').strip().split()[-1]

        message = f'Author: {author}\nCommit ID: {commit_id}\nMessage: {commit_message}\n\n'

        for key, value in self.data.items():
            message += f"Образ: {key}\nРезультат сборки: {'Успешно' if value['status'] else value['message']}" \
                       f"\nВерсия релиза: {value['builder_release']}\nДата сборки: {self.datetime}\n\n"

        data_to_load.update({'author': author, 'commit_message': commit_message, 'commit_id': commit_id,
                             'assembly': self.data, 'date': self.datetime})

        try:
            self.load_in_database(data_to_load)
        except Exception as error:
            print(error)

        return message

    def send(self):
        message = self.prepare()
        self.bot.send_message(self.chat_id, message, parse_mode='html')


if __name__ == "__main__":
    parser = Parser()
    status = parser.parse()
    notifier = Notifier(status)
    notifier.send()
