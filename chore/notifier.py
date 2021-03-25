import os
import requests
import subprocess

import telebot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


class Parser:

    def __init__(self):
        self.url = 'https://raw.githubusercontent.com/antonkurenkov/systembuilder_2021/develop/status.json'

    def parse(self):
        return requests.get(self.url).json()


class Notifier:

    def __init__(self, data):
        # self.chat_id = 444591160  # daniil
        self.chat_id = -414189807  # group
        self.data = list(data.values())[0]
        self.datetime = list(data.keys())[0]
        self.bot = telebot.TeleBot(TOKEN)

    def prepare(self):
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
        return message

    def send(self):
        message = self.prepare()
        self.bot.send_message(self.chat_id, message, parse_mode='html')


if __name__ == "__main__":
    parser = Parser()
    status = parser.parse()
    notifier = Notifier(status)
    notifier.send()
