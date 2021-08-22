import yaml
from pathlib import Path


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
                config.update(yaml.safe_load(f))
        
        self.generator = config['generator']
        self.parser = config['parser']
        self.output = config['output']
