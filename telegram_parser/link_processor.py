import requests, bs4, re, csv, time

def get_link(link, output, parser_type, print):
    i = 0
    while i < 5:
        try:
            url = 'https://t.me/' + link        #getting data from link
            r = requests.get(url, stream=True)  
            soup = bs4.BeautifulSoup(r.text, "html.parser") 
            type_link = str(soup.find_all('a', class_="tgme_action_button_new"))
            members_str = str(soup.find_all('div', class_="tgme_page_extra"))
            found = ''
            
            if '1' in parser_type or '2' in parser_type:
                if 'Preview channel' in type_link:      #check for channel
                    # if '1' in output or '2' in output:
                    #     print('Try: ' + link + ', result: New Channel')
                    members_int = re.findall(r'\d+', members_str)
                    members = ''
                    members = members.join(members_int)
                    try:
                        description = str(soup.find('div', class_="tgme_page_description").text).replace(';', ':')
                    except:
                        description = 'None'
                    try:
                        title = str(soup.find('div', class_="tgme_page_title").text)[1:-1].replace(';', ':')
                    except:
                        title = 'None'
                        description = 'None'
                    if members == '':
                        members = '0'
                    with open('channel_telegram_parser.csv','a',newline='') as f:
                        csv_writer=csv.writer(f)
                        csv_writer.writerow([link, title, description, members])
                    found += 'c'
                    
            if found == '':
                if '1' in parser_type or '3' in parser_type:    
                    if 'Preview channel' not in type_link and 'members' in members_str:       #check for group
                        # if '1' in output or '2' in output:
                        #     print('Try: ' + link + ', result: New Group')
                        members_str = members_str.split(',')[0]
                        members_int = re.findall(r'\d+', members_str)
                        members = ''
                        members = members.join(members_int)
                        try:
                            description = str(soup.find('div', class_="tgme_page_description").text).replace(';', ':')
                        except:
                            description = 'None'
                        try:
                            title = str(soup.find('div', class_="tgme_page_title").text)[:-1].replace(';', ':')
                        except:
                            title = 'None'
                            description = 'None'
                        if members == '':
                            members = '0'
                        with open('group_telegram_parser.csv','a',newline='') as f:
                            group_csv_writer=csv.writer(f)
                            group_csv_writer.writerow([link, title, description, members]) 
                        found += 'g'
                        
            if found == '':        
                if '1' in parser_type or '4' in parser_type:    
                    if 'tgme_action_button_new' in type_link and 'member' not in members_str and 'Send Message' in type_link:
                        # if '1' in output or '2' in output:
                        #     print('Try: ' + link + ', result: New User')
                        try:
                            description = str(soup.find('div', class_="tgme_page_description").text).replace(';', ':')
                        except:
                            description = 'None'
                        try:
                            title = str(soup.find('div', class_="tgme_page_title").text)[:-1].replace(';', ':')
                        except:
                            title = 'None'
                            description = 'None'
                        with open('user_telegram_parser.csv','a',newline='') as f:
                            group_csv_writer=csv.writer(f)
                            group_csv_writer.writerow([link, title, description]) 
                        found += 'u'
            
            if '1' in parser_type or '5' in parser_type:
                url_stickers = 'https://t.me/addstickers/' + link        #getting data from link
                r_stickers = requests.get(url_stickers, stream=True)  
                soup_stickers = bs4.BeautifulSoup(r_stickers.text, "html.parser") 
                type_link = str(soup_stickers.find_all('div', class_="tgme_page_description")).replace(u'\xa0', ' ').replace(';', ':')
                if re.search('Sticker Set', type_link):      #check for channel
                    pass 
                else:
                    # print('Try: ' + link + ', result: New Sticker Pack')
                    start_name = [(m.start(0), m.end(0)) for m in re.finditer("<strong>", type_link)][1][1]
                    end_name = [(m.start(0), m.end(0)) for m in re.finditer("</strong>", type_link)][1][0]
                    name = type_link[start_name:end_name]
                    with open('stickers_telegram_parser.csv','a',newline='') as f:
                        stickers_csv_writer=csv.writer(f)
                        stickers_csv_writer.writerow([link, name]) 
                    found += 's'
            if '1' in output or '2' in output:
                if found != '':
                    mess = ''
                    if 'c' in found:
                        mess += 'Channel, '
                    if 'g' in found:
                        mess += 'Group, '
                    if 'u' in found:
                        mess += 'User, '
                    if 's' in found:
                        mess += 'Sticker Pack, '
                else:
                    mess = 'False'
                print('Try: ' + link + ', result: ' + mess)
            return
        except OSError:         #exceptions
            if i != 4:    
                print('No connection. Pause script')
            if i == 4:
                print('Connection error. Stop script.')
                return 'connection_error'
            i += 1
            time.sleep(10)