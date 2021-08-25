import re

import requests
from more_itertools import consume, nth


class Basic:
    def parse(self, link):
        if link['type'] == 'stickers':
            return self.parse_stickers(link['link'])
        if link['type'] == 'user':
            return self.parse_user(link['link'])
        if link['type'] == 'bot':
            return self.parse_bot(link['link'])
        raise NotImplementedError(f'Type {link["type"]} not implemented')

    def parse_stickers(self, link):
        f_link = f'https://t.me/addstickers/{link}'
        with requests.get(f_link, stream=True) as res:
            lines = res.iter_lines()
            consume(lines, 7)
            line = next(lines)
            if line.startswith(b'<meta property="og:title" content="Add sticker set on'):
                return None
            return {
                'type': 'stickers',
                'link': f_link
            }

    def parse_bot(self, link):
        f_link = f'https://t.me/{link}'
        with requests.get(f_link, stream=True) as res:
            lines = res.iter_lines()
            if not check_exists(lines):
                return None
            return {
                'type': 'bot',
                'link': f_link
            }

    def parse_user(self, link):
        f_link = f'https://t.me/{link}'
        with requests.get(f_link, stream=True) as res:
            lines = res.iter_lines()
            if not check_exists(lines):
                return None
            consume(lines, 60)
            consumewhile(lines, lambda x: x.startswith(b'<!--'))
            line = next(lines)
            if line.startswith(b'<!-- P'):
                return {
                    'type': 'user',
                    'link': f_link
                }
            if line.startswith(b'<div class="tgme_page_action'):
                return {
                    'type': 'channel',
                    'link': f_link
                }
            return {
                'type': 'group',
                'link': f_link
            }
        return None


def check_exists(lines):
    robots = nth(lines, 6)
    if robots.startswith(b'    <meta name="r'):
        return False
    return True


def consumewhile(it, fun):
    n = next(it)
    while not fun(n):
        n = next(it)
    return n


class FullInfo:
    def parse(self, link):
        # if link['type'] == 'stickers':
        #     return self.parse_stickers(link['link'])
        if link['type'] == 'user':
            return self.parse_user(link['link'])
        # if link['type'] == 'bot':
        #     return self.parse_bot(link['link'])
        raise NotImplementedError(f'Type {link["type"]} not implemented')

    def parse_user(self, link):
        f_link = f'https://t.me/{link}'
        with requests.get(f_link, stream=True) as res:
            lines = res.iter_lines()
            if not check_exists(lines):
                return None
            title_line = next(lines)
            title = title_line[35:-2].decode()
            description_line = nth(lines, 2)
            description = description_line[41:-2].decode()
            members_line = consumewhile(lines, lambda x: x.startswith(
                b'<div class="tgme_page_ex'))
            consumewhile(lines, lambda x: x.startswith(b'<!--'))
            line = next(lines)
            if line.startswith(b'<!-- P'):
                return {
                    'type': 'user',
                    'link': f_link,
                    'title': title,
                    'description': description
                }
            num = re.match(rb'\d+', members_line[29:])
            if num is None:
                members = 0
            else:
                members = int(num.group(0))
            if line.startswith(b'<div class="tgme_page_action'):
                return {
                    'type': 'channel',
                    'link': f_link,
                    'title': title,
                    'description': description,
                    'members': members
                }
            return {
                'type': 'group',
                'link': f_link,
                'title': title,
                'description': description,
                'members': members
            }
        return None
