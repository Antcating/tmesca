from pathlib import Path

import yaml
from questionary import Choice, select, confirm, text, checkbox
import re


class Config:
    def __init__(self, prompt=False, filename='tmesca.yml'):
        config = {
            'generator': {},
            'parser': {},
            'output': {}
        }
        path = Path(filename)
        if path.is_file():
            with path.open('r') as f:
                s = yaml.safe_load(f)
                print(s)
                config.update(s)

        self._generator = config['generator'] or dict()
        self._parser = config['parser'] or dict()
        self._output = config['output'] or dict()

        if prompt:
            self.generator_prompt()
            self.parser_prompt()

        # self.postprocessing
        # self.init_session()

    def generator_prompt(self):
        gen = self._generator
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
        par = self._parser
        que = QUESTIONS['parser']
        if 'type' not in par:
            par['type'] = que['type'].ask()
        if 'info' not in par:
            par['info'] = que['info'].ask()
        if 'filter' not in par:
            par['filter'] = que['filter'].ask()
        
    def output_prompt(self):
        out = self._output
        que = QUESTIONS['output']
        if 'type' not in out:
            out['type'] = que['type'].ask()
        if out['type'] is not 'none' and 'filter' not in out:
            out['filter'] = que['filter'].ask()

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
            validate=lambda x: re.match(r'^\d+$', x) is not None
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
