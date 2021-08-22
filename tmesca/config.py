from pathlib import Path

import yaml
from questionary import Choice, select, confirm, text
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

        self.generator = config['generator'] or dict()
        self.parser = config['parser'] or dict()
        self.output = config['output'] or dict()

        if prompt:
            self.generator_prompt()
            
        # self.postprocessing
        # self.init_session()

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
    }
}
