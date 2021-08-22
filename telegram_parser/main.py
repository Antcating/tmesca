# -*- coding: utf-8 -*-
import time
import sys
from database_check import database_check, fast_database_check
from link_processor import get_link, get_fast_link, telegram_parser_open, fast_telegram_parser_open
from link_generator import random_addresses, linear_addresses
from print_handler import print_func
from database import Database
from new_search import check_links


def program_exit(link, parser_config):
    """Exiting the program.

        Args:
            link: [str] last link, script was working with.\n
            parser_config: [dict] get one of the possibilities: linear, random of mutated
            and make last preparation before ending the program.
    """
    if parser_config['work_mode'] == '1':  # 1 = linear
        save_msg = 'Saving last linear link position'
        print_func(parser_config, save_msg)
        open('.last_link', 'w').write(link)
    stop_msg = 'Script stopped'
    print_func(parser_config, stop_msg)
    sys.exit(0)


def main(parser_config):
    # database_check(parser_config)
    # fast_database_check()
    # channel_db, group_db, user_db, stickers_db, bot0_db, bot1_db = telegram_parser_open()
    # channel_fast_db, group_fast_db, user_fast_db, stickers_fast_db, bot0_fast_db, bot1_fast_db = fast_telegram_parser_open()
    db = Database(parser_config['fast_mode'] == '1', parser_config)
    try:
        start_message = 'Parser is started!'
        print_func(parser_config, start_message)
        if parser_config['work_mode'] == '1':  # 1 = linear
            with open('.last_link') as f:
                seed = f.read()
            links = linear_addresses(seed)
        elif parser_config['work_mode'] == '2':  # 2 = random
            links = random_addresses()

        for link in links:
            url_get_status = ''
            if parser_config['fast_mode'] == '0':
                url_get_status = get_link(link,
                                          parser_config,
                                          db)
            elif parser_config['fast_mode'] == '1':
                url_get_status = get_fast_link(link,
                                               parser_config,
                                               db)
            elif parser_config['fast_mode'] == '2':
                url_get_status = check_links(link,
                                             parser_config,
                                             channel_fast_db,
                                             group_fast_db,
                                             user_fast_db,
                                             stickers_fast_db,
                                             bot0_fast_db,
                                             bot1_fast_db)

            if url_get_status == 'connection_error':
                program_exit(link, parser_config)
            if parser_config['turbo_mode'] == '0':
                time.sleep(1.5)
            else:
                continue

    except KeyboardInterrupt:
        if parser_config['work_mode'] == '3':
            err_msg = 'Mutation checking keyboard interrupted'
            print_func(parser_config, err_msg)
        program_exit(link, parser_config)
