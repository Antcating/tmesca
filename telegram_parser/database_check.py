import csv, os

def database_check(print):
    database_names_list = [
        'channel_telegram_parser.csv',
        'group_telegram_parser.csv',
        'user_telegram_parser.csv',
        'stickers_telegram_parser.csv',
        'bots_telegram_parser.csv',
        ]
    for database_name in database_names_list:
        try:                                                                    # checking existing of the telegram_parser.csv file
            open('output/' + database_name, 'r').close()
        except FileNotFoundError:
            try:
                os.mkdir('output')
            except FileExistsError:
                pass
            open('output/' + database_name, 'a+')
            with open('output/' + database_name,'a',newline='') as f:
                csv_writer=csv.writer(f)
                if 'group' in database_name or 'channel' in database_name:
                    csv_writer.writerow(['adress', 'title', 'description', 'members'])
                elif 'user' in database_name or 'bots' in database_name:
                    csv_writer.writerow(['adress', 'title', 'description'])
                else:
                    csv_writer.writerow(['adress', 'name'])
            print('Init Info:' + database_name + ' was created in the script folder')
        
            