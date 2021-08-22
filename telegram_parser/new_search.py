import requests
import time
from more_itertools import consume
from itertools import dropwhile
from link_processor import output_func, print_func, fast_telegram_parser
from threading import Thread
from concurrent.futures import ThreadPoolExecutor


def check_stickers(link):
    with requests.get(f'https://t.me/addstickers/{link}') as res:
        lines = res.iter_lines()
        consume(lines, 7)
        line = next(lines)
        if line.startswith(b'<meta property="og:title" content="Add sticker set on'):
            return ''
        return 's,'


def check_bot(link, succ):
    with requests.get(f'https://t.me/{link}', stream=True) as res:
        lines = res.iter_lines()
        if not check_exists(lines):
            return ''
        return succ


def check_user(link):
    with requests.get(f'https://t.me/{link}', stream=True) as res:
        lines = res.iter_lines()
        if not check_exists(lines):
            return ''
        consume(lines, 60)
        lines = dropwhile(lambda x: not x.startswith(b'<!--'), lines)
        consume(lines, 1)
        line = next(lines)
        if line.startswith(b'<!-- P'):
            return 'u,'
        if line.startswith(b'<div class="tgme_page_action'):
            return 'c,'
        return 'g,'
    return ''


def check_exists(lines):
    consume(lines, 6)
    robots = next(lines)
    if robots.startswith(b'    <meta name="r'):
        return False
    return True


def check_links(link, parser_config, db):
    for i in range(5):
        try:
            found = ''
            found_b = ''
            found_sgu = ''
            found_s = ''
            _found_b = ''
            if any(parser_mode in parser_config['parser_type'] for parser_mode in ['1', '2', '3', '4', '5', '6']):
                with ThreadPoolExecutor(max_workers=6) as executor:
                    if any(parser_mode in parser_config['parser_type'] for parser_mode in ['1', '2', '3', '4']):
                        channel_group_user_future = executor.submit(
                            check_user, link)
                    if any(parser_mode in parser_config['parser_type'] for parser_mode in ['1', '5']):
                        sticker_future = executor.submit(check_stickers, link)
                    if any(parser_mode in parser_config['parser_type'] for parser_mode in ['1', '6']):
                        if '1' in parser_config['bot_mode']:
                            _bot_future = executor.submit(
                                check_bot, link + '_bot', 'b0,')
                        if '2' in parser_config['bot_mode']:
                            bot_future = executor.submit(
                                check_bot, link + 'bot', 'b1,')

            if any(parser_mode in parser_config['parser_type'] for parser_mode in ['1', '2', '3', '4']):
                found_sgu = channel_group_user_future.result()
                if any(parser_mode in parser_config['parser_type'] for parser_mode in ['1', '2']):
                    found_sgu = found_sgu.replace('c,', '')
                if any(parser_mode in parser_config['parser_type'] for parser_mode in ['1', '3']):
                    found_sgu = found_sgu.replace('g,', '')
                if any(parser_mode in parser_config['parser_type'] for parser_mode in ['1', '4']):
                    found_sgu = found_sgu.replace('u,', '')
            if any(parser_mode in parser_config['parser_type'] for parser_mode in ['1', '5']):
                found_s = sticker_future.result()
            if any(parser_mode in parser_config['parser_type'] for parser_mode in ['1', '6']):
                if '1' in parser_config['bot_mode']:
                    _found_b = _bot_future.result()
                if '2' in parser_config['bot_mode']:
                    found_b = bot_future.result()

            found = found_s + found_sgu + found_b + _found_b
            Thread(target=fast_telegram_parser, args=(
                db,
                link,
                found,
            )).start()

            output_func(found, link, parser_config)

            return
        except OSError:  # exceptions
            if i != 4:
                print_func(parser_config, 'No connection. Pause script')
                time.sleep(10)

    print_func(parser_config, 'Connection error. Stop script.')
    return 'connection_error'
