#! /usr/bin/env python3
import atexit
from pathlib import Path

from tmescalib.config import Config
from tmescalib.generators import get_generator
from tmescalib.requester import Requester
from tmescalib.lighting_parser import Basic

last_link = None


def start():
    global last_link
    config = Config(True)
    requester = Requester()
    parser = Basic()
    links = get_generator(config)

    if config.generator['save_sessions']:
        atexit.register(save_session)

    for link in links:
        last_link = link
        link_types = produce_links_types(link, config)
        requester.add(link_types, handler, config, parser)

    last_link = None


def handler(link, config, parser):
    res = parser.parse(link)
    if res is None:
        return
    if res['type'] == 'user' and 'users' not in config._parser['filter']:
        return
    if res['type'] == 'group' and 'groups' not in config._parser['filter']:
        return
    if res['type'] == 'channel' and 'channels' not in config._parser['filter']:
        return
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
