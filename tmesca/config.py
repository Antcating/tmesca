import re
from pathlib import Path

import yaml
from questionary import Choice, checkbox, confirm, select, text

try:
    from .bot import init
except:
    def init(*args):
        raise NotImplementedError('Telegram bot not works')

class Config:
    def __init__(self, prompt=False, filename='tmesca.yml'):
        config = {
            'generator': {},
            'parser': {},
            'output': {},
            'misc': {}
        }
        path = Path(filename)
        if path.is_file():
            with path.open('r') as f:
                s = yaml.safe_load(f)
                config.update(s)

        self.generator = config['generator'] or dict()
        self.parser = config['parser'] or dict()
        self.output = config['output'] or dict()
        self.misc = config['misc'] or dict()

        if prompt:
            self.generator_prompt()
            self.parser_prompt()
            self.output_prompt()

        self.postprocessing()
        self.init_session()

    def generator_prompt(self):
        gen = self.generator
        que = QUESTIONS['generator']
        if 'type' not in gen:
            gen['type'] = que['type'].ask()

        if gen['type'] == 'linear':
            last_link = Path('.last_link')
            if last_link.is_file() and 'restore_sessions' not in gen:
                gen['restore_sessions'] = que['restore_sessions'].ask()
            if (not last_link.is_file() or not gen['restore_sessions']) and 'link_length' not in gen:
                gen['link_length'] = int(que['link_length'].ask())

    def parser_prompt(self):
        par = self.parser
        que = QUESTIONS['parser']
        if 'type' not in par:
            par['type'] = que['type'].ask()
        if 'info' not in par:
            par['info'] = que['info'].ask()
        if 'filter' not in par:
            par['filter'] = que['filter'].ask()

    def output_prompt(self):
        out = self.output
        que = QUESTIONS['output']
        if 'type' not in out:
            out['type'] = que['type'].ask()
        if out['type'] != 'none' and 'filter' not in out:
            out['filter'] = que['filter'].ask()

    def postprocessing(self):
        if 'save_sessions' not in self.generator:
            self.generator['save_sessions'] = True

        if isinstance(self.parser['filter'], str):
            res = self.parser['filter']
            if res == 'all':
                res = ['users', 'groups', 'channels', 'bots', 'stickers']
            else:
                res = [res]
            self.parser['filter'] = set(res)
        else:
            self.parser['filter'] = set(self.parser['filter'])

        if 'bot_suffix' not in self.parser:
            self.parser['bot_suffix'] = ['_bot', 'bot']
        elif isinstance(self.parser['bot_suffix'], str):
            self.parser['bot_suffix'] = [res]

        if 'custom_suffix' not in self.parser:
            self.parser['custom_suffix'] = ['']
        elif isinstance(self.parser['custom_suffix'], str):
            self.parser['custom_suffix'] = [res]

        if 'slow_mode' not in self.parser:
            self.parser['slow_mode'] = 0
        
        if 'single_thread' not in self.misc:
            self.misc['single_thread'] = False

    def init_session(self):
        self.session = {}
        last_link = Path('.last_link')
        if self.generator['type'] == 'linear':
            if last_link.is_file() and self.generator['restore_sessions']:
                self.session['seed'] = last_link.read_text()
            else:
                self.session['seed'] = 'a' * self.generator['link_length']

        if self.output['type'] == 'telegram':
            if 'bot_token' not in self.output or 'user_id' not in self.output:
                raise Exception('No user_id or bot_token in config')
            self.session['bot'] = init(
                self.output['bot_token'], self.output['user_id'])

    def print(self, message):
        if self.output['type'] == 'console':
            print(message)
        elif self.output['type'] == 'telegram':
            self.session['bot'].send_message(self.output['user_id'], message)

    def print_link(self, res):
        s = [f'{k}: {v}' for k, v in res.items()]
        self.print('\n'.join(s))

    def print_everything(self, message):
        if self.output['filter'] == 'everything':
            self.print(message)


QUESTIONS = {
    'generator': {
        'type': select(
            message='Choose link generation method:',
            choices=[
                Choice('Linear', 'linear'),
                Choice('Random', 'random')
            ]
        ),
        'restore_sessions': confirm(
            message='Continue old session?',
            default=True
        ),
        'link_length': text(
            message='Enter link length:',
            validate=lambda x: re.match(
                r'^\d+$', x) is not None and int(x) >= 5
        )
    },
    'parser': {
        'type': select(
            message='Choose parser:',
            choices=[
                Choice('Soup. Parses page with BS4', 'soup'),
                Choice('Lighting. No parsing, just some string checks', 'lighting')
            ]
        ),
        'info': select(
            message='Choose information to collect: ',
            choices=[
                Choice('Full information', 'full'),
                Choice('Only link', 'link')
            ]
        ),
        'filter': checkbox(
            message='Choose content to find:',
            choices=[
                Choice('Users', 'users'),
                Choice('Channels', 'channels'),
                Choice('Groups', 'groups'),
                Choice('Bots', 'bots'),
                Choice('Stickerpacks', 'stickers')
            ]
        )
    },
    'output': {
        'type': select(
            message='Choose where to output:',
            choices=[
                Choice('Console', 'console'),
                Choice('Telegram', 'telegram'),
                Choice('None', 'none')
            ]
        ),
        'filter': select(
            message='Choose information to output: ',
            choices=[
                Choice('Everything', 'everything'),
                Choice('Finds only', 'basic')
            ]
        )
    }
}
