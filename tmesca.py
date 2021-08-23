#! /usr/bin/env python3
import atexit
from pathlib import Path

from tmescalib.config import Config
from tmescalib.generators import get_generator

last_link = None


def start():
    global last_link
    config = Config(True)
    links = get_generator(config)

    if config.generator['save_sessions']:
        atexit.register(save_session)

    for link in links:
        last_link = link
        link_types = produce_links_types(link, config)
        # print(link)
    last_link = None


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
    if 'users' in filters or 'groups' in filters or 'channels' in filters:
        res.append({
            'type': 'user',
            'link': link
        })
    if 'bots' in filters:
        for suffix in config.parser['bot_suffix']:
            res.append({
                'type': 'bot',
                'link': link + suffix
            })
    if 'stickers' in filters:
        res.append({
            'type': 'stickers',
            'link': link
        })
    return res

if __name__ == '__main__':
    start()
