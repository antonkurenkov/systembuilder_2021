import os
import subprocess
import requests
import telebot

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

class Parser:

    def __init__(self):
        self.current_branch = None
        self.author_name = None
        self.commit_message = None
        self.commit_id = None
        self.file = None

    def get_current_branch(self):
        # get current branch's name
        # get the author of the last commit
        # get commit message
        subprocess.run(['git', 'clone', '--bare', 'https://github.com/antonkurenkov/systembuilder_2021.git', 'tmdir'],
                       stdout=subprocess.PIPE)

        self.current_branch = subprocess.run(['git', 'branch', '--show-current'], cwd='tmdir/', stdout=subprocess.PIPE)\
            .stdout.decode("utf-8").strip('\n')

        info = subprocess.run(['git', 'log', '-1', '--pretty=format:"%an - %s"'], cwd='tmdir/', stdout=subprocess.PIPE)\
            .stdout.decode("utf-8")
        self.author_name, self.commit_message = info.strip('"').split('-')

        self.commit_id = subprocess.run(['git', 'log', '-1', '--pretty=oneline'], cwd='tmdir/', stdout=subprocess.PIPE) \
            .stdout.decode("utf-8").split()[0]

        return (self.current_branch, self.author_name, self.commit_message)

    def get_status(self):
        self.file = requests.get('https://raw.githubusercontent.com/antonkurenkov/systembuilder_2021/'
                            f'{self.current_branch}/status.json')
        return self.file.json()

class Notifier(Parser):

    def __init__(self):
        super().__init__()
        self.final_string = None
        # test chat id
        self.chat_id = -409732306

    def prepare(self):
        self.final_string = f"""{self.commit_id}\n{self.author_name}\n{self.commit_message.strip()}"""

        return self.final_string

    def send_message(self):
        bot.send_message(self.chat_id, self.final_string)


# instance = Notifier()
# instance.get_current_branch()
# instance.prepare()
# instance.send_message()