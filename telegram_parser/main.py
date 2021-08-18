# -*- coding: utf-8 -*-
import time, sys
from database_check import database_check, fast_database_check
from link_processor import get_link, get_fast_link, telegram_parser_open, fast_telegram_parser_open
from link_generator import alphabets_generator, random_address_generator, linear_address_generator, \
    last_link_read_linear_address
from print_handler import print_func


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
    database_check(parser_config)
    fast_database_check()
    channel_db, group_db, user_db, stickers_db, bot0_db, bot1_db = telegram_parser_open()
    channel_fast_db, group_fast_db, user_fast_db, stickers_fast_db, bot0_fast_db, bot1_fast_db = fast_telegram_parser_open()
    alphabet, alphabet1, alphabet_last = alphabets_generator()
    if parser_config['work_mode'] == '1':
        linear_letter_link_ids_array = last_link_read_linear_address(alphabet, alphabet1, alphabet_last)


    try:
        start_message = 'Parser is started!'
        print_func(parser_config, start_message)
        while True:
            if parser_config['work_mode'] == '1':  # 1 = linear
                link = linear_address_generator(alphabet, alphabet1, alphabet_last,\
                                                linear_letter_link_ids_array,  parser_config)
            elif parser_config['work_mode'] == '2':  # 2 = random
                link = random_address_generator(alphabet, alphabet1, alphabet_last)

            if parser_config['fast_mode'] == '0':
                url_get_status = get_link(link,
                                          parser_config,
                                          channel_db,
                                          group_db,
                                          user_db,
                                          stickers_db,
                                          bot0_db,
                                          bot1_db)
            elif parser_config['fast_mode'] == '1':
                url_get_status = get_fast_link(link,
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
