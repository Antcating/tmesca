from itertools import dropwhile

import requests
from more_itertools import consume


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
                return ''
            consume(lines, 60)
            lines = dropwhile(lambda x: not x.startswith(b'<!--'), lines)
            consume(lines, 1)
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
    consume(lines, 6)
    robots = next(lines)
    if robots.startswith(b'    <meta name="r'):
        return False
    return True
