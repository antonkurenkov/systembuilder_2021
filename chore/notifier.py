import os
import subprocess
import requests
import telebot

# do not forget to add token to the environment variables

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)


class Parser:

    def __init__(self):
        self.current_branch = None
        self.author_name = None
        self.commit_message = None
        self.commit_id = None
        self.file = None

        self.chat_id = -414189807  # group
        # self.chat_id = 417554679  # anton

    def get_current_branch(self):
        # get current branch's name
        # get the author of the last commit
        # get commit message
        # subprocess.run(['git', 'clone', '--bare', 'https://github.com/antonkurenkov/systembuilder_2021.git', 'tmdir'],
        #               stdout=subprocess.PIPE)

        self.current_branch = subprocess.run(['git', 'branch', '--show-current'], stdout=subprocess.PIPE)\
            .stdout.decode("utf-8").strip('\n')

        info = subprocess.run(['git', 'log', '-2', '--pretty=format:"%an - %s"'], stdout=subprocess.PIPE)\
            .stdout.decode("utf-8").split('\n')[-1]
        self.author_name, self.commit_message = info.strip('"').split('-')

        self.commit_id = subprocess.run(['git', 'log', '-1', '--pretty=oneline'], stdout=subprocess.PIPE) \
            .stdout.decode("utf-8").split()[0]

        return self.current_branch, self.author_name, self.commit_message, self.commit_id

    def get_status(self):
        try:
            info = self.get_current_branch()
            self.file = requests.get('https://raw.githubusercontent.com/antonkurenkov/systembuilder_2021/'
                                f'{info[0]}/status.json')
            return self.file.json()
        except Exception as e:
            bot.send_message(self.chat_id, e)


class Notifier(Parser):

    def __init__(self):
        super().__init__()
        self.final_string = None

    def prepare(self):
        info = self.get_current_branch()
        self.final_string = f"""{info[3]}\n{info[1]}\n{info[2].strip()}"""
        return self.final_string

    def send_message(self):
        final_string = self.prepare()
        bot.send_message(self.chat_id, final_string)


instance = Notifier()
instance.get_current_branch()
instance.prepare()
instance.send_message()