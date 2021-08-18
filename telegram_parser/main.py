import time, sys
from database_check import database_check, fast_database_check
from link_processor import get_link, get_fast_link, telegram_parser_open, fast_telegram_parser_open
from link_generator import alphabets_generator, random_address_generator, linear_address_generator, \
    last_link_read_linear_address, mutation_address_generator


def program_exit(link, parser_config):
    """Exiting the program.

        Args:
            link: [str] last link, script was working with.\n
            parser_config: [dict] get one of the possibilities: linear, random of mutated
            and make last preparation before ending the program.
    """
    if parser_config['work_mode'] == '1':  # 1 = linear
        print('Saving last linear link position')
        open('.last_link', 'w').write(link)
    print('Script stopped')
    sys.exit(0)


def main(parser_config):
    database_check(print)
    fast_database_check(print)
    channel_db, group_db, user_db, stickers_db, bot0_db, bot1_db = telegram_parser_open()
    channel_fast_db, group_fast_db, user_fast_db, stickers_fast_db, bot0_fast_db, bot1_fast_db = fast_telegram_parser_open()
    alphabet, alphabet1, alphabet_last = alphabets_generator()
    if parser_config['work_mode'] == '1':
        linear_letter_link_ids_array = last_link_read_linear_address(alphabet, alphabet1, alphabet_last)

    elif parser_config['work_mode'] == '3':
        if mutated_initial_link != None:
            mutated_array = mutation_address_generator(mutated_initial_link)
            total_mutated_rows = len(mutated_array)
            print('Total mutation created: ', total_mutated_rows)
            mutated_word_id = 0
        else:
            print('Error! Initial mutation word is not found!')
            program_exit('undef', work_mode, window)

    try:
        print('Parser is started!')
        while True:
            if parser_config['work_mode'] == '1':  # 1 = linear
                link = linear_address_generator(alphabet, alphabet1, alphabet_last, linear_letter_link_ids_array, print)
            elif parser_config['work_mode'] == '2':  # 2 = random
                link = random_address_generator(alphabet, alphabet1, alphabet_last)
            elif parser_config['work_mode'] == '3':  # 3 = mutation
                if total_mutated_rows > mutated_word_id + 1:
                    link = mutated_array[mutated_word_id]
                    mutated_word_id += 1
                else:
                    program_exit(link, parser_config)

            if fast_mode == False:
                url_get_status = get_link(link,
                                          output,
                                          parser_type,
                                          bot_mode,
                                          print,
                                          channel_db,
                                          group_db,
                                          user_db,
                                          stickers_db,
                                          bot0_db,
                                          bot1_db)
            else:
                url_get_status = get_fast_link(link,
                                               output,
                                               parser_type,
                                               bot_mode,
                                               print,
                                               channel_fast_db,
                                               group_fast_db,
                                               user_fast_db,
                                               stickers_fast_db,
                                               bot0_fast_db,
                                               bot1_fast_db)

            if url_get_status == 'connection_error':
                program_exit(link, parser_config)

            # if window != False:
            #     window.Refresh()
            #     event, values = window.read(timeout=0.0001)
            #     # if event in ("Exit",sg.WIN_CLOSED):
            #     #     program_exit(link, work_mode, window)
            #     if event == 'stop_program':
            #         if work_mode == '1':  # 1 = linear
            #             print('Saving last linear link position')
            #             open('.last_link', 'w').write(link)
            #         print('Parser stoped')
            #         break
            if parser_config['turbo_mode'] == False:
                time.sleep(1.5)
            else:
                continue

    except KeyboardInterrupt:
        if parser_config['work_mode'] == '3':
            print('Mutation checking keyboard interrupted')
        program_exit(link, parser_config)
