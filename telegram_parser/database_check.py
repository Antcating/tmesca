import csv 

def database_check(print):
    try:                                                                    # checking existing of the telegram_parser.csv file
        open('output/channel_telegram_parser.csv', 'r').close()
    except FileNotFoundError:
        open('output/channel_telegram_parser.csv', 'a+')
        with open('output/channel_telegram_parser.csv','a',newline='') as f:
            csv_writer=csv.writer(f)
            csv_writer.writerow(['adress', 'title', 'description', 'members'])
        print('Init Info: Channel database was created in the script folder')
        
            
    try:                                                                    # checking existing of the group_telegram_parser.csv file
        open('output/group_telegram_parser.csv', 'r').close()
    except FileNotFoundError:
        with open('output/group_telegram_parser.csv','a',newline='') as f:
            csv_writer=csv.writer(f)
            csv_writer.writerow(['adress', 'title', 'description', 'members'])
        print('Init Info: Group database was created in the script folder')
        
    try:                                                                    # checking existing of the group_telegram_parser.csv file
        open('output/user_telegram_parser.csv', 'r').close()
    except FileNotFoundError:
        with open('output/user_telegram_parser.csv','a',newline='') as f:
            csv_writer=csv.writer(f)
            csv_writer.writerow(['adress', 'title', 'description'])
        print('Init Info: User database was created in the script folder')
        
    try:                                                                    # checking existing of the stickers_telegram_parser.csv file
        open('output/stickers_telegram_parser.csv', 'r').close()
    except FileNotFoundError:
        with open('output/stickers_telegram_parser.csv','a',newline='') as f:
            csv_writer=csv.writer(f)
            csv_writer.writerow(['adress', 'name'])
        print('Init Info: Sticker database was created in the script folder')
        
    try:                                                                    # checking existing of the bots_telegram_parser.csv file
        open('output/bots_telegram_parser.csv', 'r').close()
    except FileNotFoundError:
        with open('output/bots_telegram_parser.csv','a',newline='') as f:
            csv_writer=csv.writer(f)
            csv_writer.writerow(['adress', 'name', 'description'])
        print('Init Info: Bot database was created in the script folder')