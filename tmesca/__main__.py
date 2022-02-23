#! /usr/bin/env python3
import atexit
from pathlib import Path

from .config import Config
from .database import Database
from .generators import get_generator
from .lighting_parser import Basic as BasicLighting
from .lighting_parser import FullInfo as FullInfoLighting
from .requester import Requester
from .soup_parser import Basic as BasicSoup
from .soup_parser import FullInfo as FullInfoSoup

last_link = None


def start():
    global last_link
    config = Config(True)
    requester = Requester()
    parser = get_parser(config)
    db = Database(config.parser['info'] == 'link')
    links = get_generator(config)

    if config.generator['save_sessions'] and config.generator['type'] == 'linear':
        atexit.register(save_session)

    for link in links:
        config.print_everything(f'Start processing link {link}')
        last_link = link
        link_types = produce_links_types(link, config)
        requester.add(link_types, handler, config, parser, db)

    last_link = None


def handler(link, config, parser, db):
    res = parser.parse(link)
    if res is None:
        return
    if res['type'] == 'user' and 'users' not in config.parser['filter']:
        return
    if res['type'] == 'group' and 'groups' not in config.parser['filter']:
        return
    if res['type'] == 'channel' and 'channels' not in config.parser['filter']:
        return

    db.add(res)
    config.print_link(res)

def save_session():
    path = Path('.last_link')
    if last_link is None:
        if path.is_file():
            path.unlink()
    else:
        path.write_text(last_link)


def produce_links_types(link, config):
    filters = config.parser['filter']
    res = []
    for prefix in config.parser['custom_prefix']:
        for suffix in config.parser['custom_suffix']:
            full_link = prefix + link + suffix
            if 'users' in filters or 'groups' in filters or 'channels' in filters:
                res.append({
                    'type': 'user',
                    'link': full_link
                })
            if 'bots' in filters:
                for bot_suffix in config.parser['bot_suffix']:
                    new_link = full_link + bot_suffix
                    if len(new_link) > 32:
                        continue
                    res.append({
                        'type': 'bot',
                        'link': new_link
                    })
            if 'stickers' in filters:
                res.append({
                    'type': 'stickers',
                    'link': full_link
                })
    return res

def get_parser(config):
    t = config.parser['type']
    i = config.parser['info']
    if t == 'soup':
        if i == 'link':
            return BasicSoup()
        if i == 'full':
            return FullInfoSoup()
        raise NotImplementedError()
    if t == 'lighting':
        if i == 'link':
            return BasicLighting()
        if i == 'full':
            return FullInfoLighting()
        raise NotImplementedError()

# if __name__ == '__main__':
#     start()
start()
