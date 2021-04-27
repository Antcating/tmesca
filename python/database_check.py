import csv 

def database_check():
    try:                                                                    # checking existing of the telegram_parser.csv file
        open('telegram_parser.csv', 'r').close()
    except:
        open('telegram_parser.csv', 'a+')
        with open('telegram_parser.csv','a',newline='') as f:
            csv_writer=csv.writer(f)
            csv_writer.writerow(['adress', 'title', 'description', 'members'])
        print('Init Info: Channel database was created in the script folder')
        
            
    try:                                                                    # checking existing of the group_telegram_parser.csv file
        open('group_telegram_parser.csv', 'r').close()
    except:
        with open('group_telegram_parser.csv','a',newline='') as f:
            csv_writer=csv.writer(f)
            csv_writer.writerow(['adress', 'title', 'description', 'members'])
        print('Init Info: Group database was created in the script folder')