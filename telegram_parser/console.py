# -*- coding: utf-8 -*-
import os
import re
import telebot
import configparser
import questionary
from main import main
from pathlib import Path


def telegram_config_creation(parser_config):
    telegram_config = configparser.ConfigParser()
    telegram_config.add_section('Telegram')
    telegram_config['Telegram']['user_id'] = parser_config['user_id']
    telegram_config['Telegram']['tg_token'] = parser_config['tg_token']
    with open('telegram.ini', 'w') as configfile:
        telegram_config.write(configfile)


# def config_creation(parser_config):
#     config = configparser.ConfigParser()
#     config.add_section('Internal')
#     config['Internal']['parser_type'] = parser_config['parser_type']
#     config['Internal']['bot_mode'] = parser_config['bot_mode']
#     config['Internal']['work_mode'] = parser_config['work_mode']
#     config['Internal']['turbo_mode'] = parser_config['turbo_mode']
#     config['Internal']['output_source'] = parser_config['output_source']
#     config['Internal']['output'] = parser_config['output']
#     with open('config.ini', 'w') as configfile:
#         config.write(configfile)


def telegram_update_config(config_element):
    config_element.read('telegram.ini')
    return config_element


def telegram_channel_settings():
    try:
        config_element = configparser.ConfigParser()
        config = telegram_update_config(config_element)
        tg_token = config['Telegram']['tg_token']

        bot = telebot.TeleBot(tg_token)
        user_id = config['Telegram']['user_id']
        try:
            bot.send_message(user_id, 'Bot test message')
        except telebot.apihelper.ApiException as telebot_error:
            if telebot_error.result.status_code == 404:
                print('Telegram config incorrect. Aborting script...')
                os.abort()

        return tg_token, bot, user_id
    except KeyError:
        print('Config does not exist. Aborting script...')
        os.abort()


def start_link():
    n_letters = input('How many letters in the link might be (at least 5): ')
    start_point = 'a' * int(n_letters)
    open('.last_link', 'w').write(start_point)


QUESTIONS = [
    {
        'type': 'checkbox',
        'name': 'parser_type',
        'message': 'What type of content do you want to parse?',
        'choices': [
            {
                'name': 'All',
                'value': '1'
            }, {
                'name': 'Channels',
                'value': '2'
            }, {
                'name': 'Groups',
                'value': '3'
            }, {
                'name': 'Users',
                'value': '4'
            }, {
                'name': 'Stickers',
                'value': '5'
            }, {
                'name': 'Bots',
                'value': '6'
            }
        ],
        'validate': lambda x: len(x) > 0,
        'filter': lambda x: ''.join(x)
    }, {
        'type': 'checkbox',
        'name': 'bot_mode',
        'message': 'Choose bot link types to parse: ',
        'choices': [
            {
                'name': 'LINK_bot',
                'value': '1'
            },
            {
                'name': 'LINKbot',
                'value': '2'
            }
        ],
        'when': lambda data: '1' in data['parser_type'] or '6' in data['parser_type'],
        'validate': lambda x: len(x) > 0,
        'filter': lambda x: ''.join(x),
    }, {
        'type': 'select',
        'name': 'work_mode',
        'message': 'What type of parsing you want to use?',
        'choices': [
            {
                'name': 'Linear parsing',
                'value': '1'
            }, {
                'name': 'Random parsing',
                'value': '2'
            }
        ]
    },
    {
        'type': 'confirm',
        'name': 'turbo_mode',
        'message': 'Turn on turbo mod (disabling timeouts between requests)?',
        'default': True,
        'filter': lambda x: '1' if x else '0'
    },
    {
        'type': 'select',
        'name': 'output',
        'message': 'What type of output do you want?',
        'choices': [
            {
                'name': 'All output (not False will be only the content, that was choosed to parse)',
                'value': '1'
            }, {
                'name': 'If something found',
                'value': '2'
            }, {
                'name': 'No output',
                'value': '3'
            }
        ]
    },
    {
        'type': 'select',
        'name': 'output_source',
        'message': 'What output source do you want?',
        'choices': [
            {
                'name': 'Console',
                'value': '1'
            }, {
                'name': 'Telegram',
                'value': '2'
            }
        ]
    }, {
        'type': 'select',
        'name': 'fast_mode',
        'message': 'Choose parser mode and speen',
        'choices': [
            {
                'name': 'Slow. Full info about page.',
                'value': '0'
            }, {
                'name': 'Fast. Only type of links check.',
                'value': '1'
            }, {
                'name': 'Lightning. No parsing of the entire page.'
            }
        ],
        'default': {
            'name': 'Fast. Only type of links check.',
            'value': '1'
        }
    }, {
        'type': 'confirm',
        'name': 'continue',
        'message': 'Continue old session?',
        'when': lambda x: x['work_mode'] == '1' and Path('.last_link').is_file()
    }, {
        'type': 'input',
        'name': 'link_length',
        'message': 'How many letters in the link might be (at least 5)?',
        'validate': lambda x: re.match(r'^\d+$', x) is not None and int(x) >= 5,
        'filter': lambda x: int(x),
        'when': lambda x: x['work_mode'] == '1' and ('continue' not in x or not x['continue'])
    }
]


def console_menu():
    parser_config = questionary.prompt(QUESTIONS)

    if len(parser_config) == 0:
        # Cancelled by user
        exit(1)

    if parser_config['output_source'] == '2':
        tg_token, bot, user_id = telegram_channel_settings()
        parser_config['bot'] = bot
        parser_config['user_id'] = user_id
        parser_config['tg_token'] = tg_token

    if 'link_length' in parser_config:
        Path('.last_link').write_text('a' * parser_config['link_length'])

    main(parser_config)


console_menu()
