import os, telebot, configparser
from main import main


def update_config(config_element):
    config_element.read('config.ini')
    return config_element


def telegram_channel_settings():
    try:
        config_element = configparser.ConfigParser()
        config = update_config(config_element)
        tg_token = config['TelegramBot']['token']

        bot = telebot.TeleBot(tg_token)
        user_id = config['Admin']['id']
        try:
            bot.send_message(user_id, 'Test message')
        except telebot.apihelper.ApiException as telebot_error:
            if telebot_error.result.status_code == 404:
                print('Telegram config incorrect. Aborting script...')
                os.abort()

        return bot, user_id
    except KeyError:
        print('Config does not exist. Aborting script...')
        os.abort()


def telegram_print_function(bot, user_id, output):
    bot.send_message(user_id, output)


def start_link():
    n_letters = input('How many letters in the link might be (at least 5): ')
    start_point = 'a' + '1' * (int(n_letters) - 1)
    open('.last_link', 'w').write(start_point)


def console_menu(print):
    parser_config = {
        'parser_type': None,
        'bot_mode': None,
        'work_mode': None,
        'turbo_mode': None,
        'output_source': None,
        'output': None,
        'print': None
    }

    def parsing_content_func(parser_config):
        parser_type = input('''
What type of content do you want to parse (input several numbers, if you want to parse any combination of content): 
 1 - All (Groups/Channel/Users
 2 - Channels
 3 - Groups
 4 - Users
 5 - Stickers
 6 - Bots
Your choice: ''')[:2].lower()
        if parser_type[0] not in ['1', '2', '3', '4', '5', '6']:
            print('Incorrect input for the parsing content types. Try again.')
            parsing_content_func(parser_config)

        if parser_type == '1' or '6' in parser_type:
            bot_mode = input('''
Choose bot link types to parse: 1/2/12:
 1 - LINK_bot
 2 - LINKbot
 12 - LINK_bot && LINKbot
Your choice: ''')
            parser_config['bot_mode'] = bot_mode
        parser_config['parser_type'] = parser_type
        return parser_config

    def work_mode_func(parser_config):
        work_mode = input('''
What type of parsing you want to use:
 1 - Linear parsing
 2 - Random parsing 
 3 - Mutation parsing 
Your choice: ''')[0].lower()
        if work_mode not in ['1', '2', '3']:
            print('Incorrect input for the work mode. Try again.')
            work_mode_func(parser_config)
        parser_config['work_mode'] = work_mode
        return parser_config

    def turbo_mode_func(parser_config):
        turbo_mode = input('Turn on turbo mod(y/n): ')[0].lower()  # work mode with/out delay
        if turbo_mode in ['y', '1']:
            parser_config['turbo_mode'] = True
        elif turbo_mode in ['n', '0']:
            parser_config['turbo_mode'] = False
        else:
            print('Incorrect input for the turbo mode. Try again.')
            turbo_mode_func(parser_config)
        return parser_config

    def output_func(parser_config):
        output = input(
'''What type of output do you want: 
 1 - All output (not False will be only the content, that was choosed to parse)
 2 - If something found
 3 - No output
Your choise: ''')[0].lower()
        if output in ['1', '2']:
            parser_config['output'] = output
            output_source = input(
'''What output source do you want: 
 1 - Console
 2 - Telegram
Your choice: ''')[0].lower()
            if output_source == '1':
                pass
            elif output_source == '2':
                bot, user_id = telegram_channel_settings()
                print = telegram_print_function
            return parser_config
        elif output == '3':
            parser_config['output'] = output
            return parser_config
        else:
            print('Incorrect input for the output. Try again.')
            output_func(parser_config)

    parser_config = parsing_content_func(parser_config)
    parser_config = work_mode_func(parser_config)
    parser_config = turbo_mode_func(parser_config)
    parser_config = output_func(parser_config)
    # fast_mode = input('Turn on only addresses write mode(y/n): ')[0].lower()
    # if fast_mode == 'y':
    #     fast_mode = True

    mutated_initial_link = None
    if parser_config['work_mode'] == '1':
        try:  # LINK Checking
            open('.last_link').read()
            change_start = input('Do you want to change number of letters in link(y/n): ')[0].lower()
            if change_start == 'y':
                start_link()
        except FileNotFoundError:
            print('Initial setup!')
            start_link()

    elif parser_config['work_mode'] == '3':
        try:
            os.remove('mutated')
        except FileNotFoundError:
            pass
        mutated_initial_link = input(
            'Input initial word to mutate (length of the word is greater than 5 letters): ').lower()
    main(parser_config)


console_menu(print)
