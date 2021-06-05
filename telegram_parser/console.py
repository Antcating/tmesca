import os, telebot
from main import main    

def telegram_channel_settings():
    try:
        tg_token = open('.telegram_token', 'r').read()
    except:
        tg_token = input('Input Telegram bot token: ')
        open('.telegram_token', 'w').write(tg_token)
    try:
        tg_address = open('.telegram_channel', 'r').read()
    except:
        tg_address = input('Input Telegram bot token: ')
        open('.telegram_channel', 'w').write(tg_address)

def telegram_print_function(output):
    tg_token = open('.telegram_token', 'r').read()
    tg_address = open('.telegram_channel', 'r').read()
    bot = telebot.TeleBot(tg_token)
    bot.send_message(tg_address, output) 
    
    

def start_link():
    n_letters = input('How many letters in the link might be (at least 5): ')
    start_point = 'a' + '1'*(int(n_letters)-1)
    open('.last_link', 'w').write(start_point)


def console_start(print):
    parser_type = input('''What type of content do you want to parse (input several numbers, if you want to parse any combination of the possible content): 
 1 - All (Groups/Channel/Users
 2 - Channels
 3 - Groups
 4 - Users
 5 - Stickers
 6 - Bots
Your choise: ''')[:2].lower()
    if parser_type == '1' or parser_type == '2':
        bot_mode = input('''Choose bot link types to parse: 1/2/12:
 1 - LINK_bot
 2 - LINKbot
 12 - LINK_bot && LINKbot
Your choise: ''')
    work_mode = input('''What type of parsing you want to use:
 1 - Linear parsing
 2 - Random parsing 
 3 - Mutation parsing 
Your choise: ''')[0].lower()
    turbo_mode = input('Turn on turbo mod(y/n): ')[0].lower()                   # work mode with/out delay
    if turbo_mode == 'y':
        turbo_mode = True
        
        
    output_source_list = input('''What output source do you want: 
 1 - Console
 2 - Telegram
Your choise: ''')[0].lower()    
    if output_source_list == '1':
        pass
    elif output_source_list == '2':
        telegram_channel_settings()
        print = telegram_print_function    



    output = input('''What type of output do you want: 
 1 - All output (not False will be only the content, that was choosed to parse)
 2 - If something found
 3 - No output
Your choise: ''')[0].lower()
    fast_mode = input('Turn on only addresses write mode(y/n): ')[0].lower()
    if fast_mode == 'y':
        fast_mode = True
    
    window = False
    mutated_initial_link = None
    if work_mode == '1':
        try:                                    # LINK Checking
            open('.last_link').read()
            change_start = input('Do you want to change number of letters in link(y/n): ')[0].lower()
            if change_start == 'y':
                start_link()
        except:
            print('Initial setup!')
            start_link()
            
    if work_mode == '3':
        try:
            os.remove('mutated')
        except:
            pass
        mutated_initial_link =  input('Input initial word to mutate (length of the word is greater than 5 letters): ').lower()
    main(work_mode, parser_type, window, turbo_mode, fast_mode, output, print, mutated_initial_link, bot_mode)
    
console_start(print)