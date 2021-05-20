import requests, bs4, re, csv, time
from threading import Thread
import concurrent.futures


def telegram_parser(link, found, title, description, members, title_stickers, bot_dict):
    if 'c' in found:
        with open('output/channel_telegram_parser.csv','a',newline='') as f:
            channel_csv_writer = csv.writer(f)
            channel_csv_writer.writerow([link, title, description, members])
    elif 'g' in found:
        with open('output/group_telegram_parser.csv','a',newline='') as f:
            group_csv_writer=csv.writer(f)
            group_csv_writer.writerow([link, title, description, members]) 
    elif 'u' in found:
        with open('output/user_telegram_parser.csv','a',newline='') as f:
            group_csv_writer=csv.writer(f)
            group_csv_writer.writerow([link, title, description]) 
    with open('output/stickers_telegram_parser.csv','a',newline='') as f:
            stickers_csv_writer=csv.writer(f)
            stickers_csv_writer.writerow([link, title_stickers]) 
    if 'b0' in found:
        with open('output/bots_telegram_parser.csv','a',newline='') as f:
            bot_csv_writer=csv.writer(f)
            bot_csv_writer.writerow([link + '_bot', bot_dict['title_bot0'], bot_dict['description_bot0']]) 
    if 'b1' in found:
        with open('output/bots_telegram_parser.csv','a',newline='') as f:
            bot_csv_writer=csv.writer(f)
            bot_csv_writer.writerow([link + 'bot', bot_dict['title_bot1'], bot_dict['description_bot1']]) 



def telegram_parser_fast(link, found):
    if 'c' in found:
        with open('output/channel_telegram_parser_fast.csv','a',newline='') as f:
            channel_csv_writer=csv.writer(f)
            channel_csv_writer.writerow([link]) 
    elif 'g' in found:
        with open('output/group_telegram_parser_fast.csv','a',newline='') as f:
            group_csv_writer=csv.writer(f)
            group_csv_writer.writerow([link]) 
    elif 'u' in found:
        with open('output/user_telegram_parser_fast.csv','a',newline='') as f:
            user_csv_writer=csv.writer(f)
            user_csv_writer.writerow([link]) 
    if 's' in found:
        with open('output/stickers_telegram_parser_fast.csv','a',newline='') as f:
            stickers_csv_writer=csv.writer(f)
            stickers_csv_writer.writerow([link]) 
    if 'b0' in found:
        with open('output/bots_telegram_parser_fast.csv','a',newline='') as f:
            bot_csv_writer=csv.writer(f)
            bot_csv_writer.writerow([link + '_bot']) 
    if 'b1' in found:
        with open('output/bots_telegram_parser_fast.csv','a',newline='') as f:
            bot_csv_writer=csv.writer(f)
            bot_csv_writer.writerow([link + 'bot']) 

def stickers_parser(link, found):
    url_stickers = 'https://t.me/addstickers/' + link        #getting data from link
    r_stickers = requests.get(url_stickers, stream=True)  
    soup_stickers = bs4.BeautifulSoup(r_stickers.text, "html.parser") 
    type_link = str(soup_stickers.find_all('div', class_="tgme_page_description")).replace(u'\xa0', ' ').replace(';', ':')
    if re.search('Sticker Set', type_link):      #check for channel
        return None, found
    else:
        # print('Try: ' + link + ', result: New Sticker Pack')
        start_name = [(m.start(0), m.end(0)) for m in re.finditer("<strong>", type_link)][1][1]
        end_name = [(m.start(0), m.end(0)) for m in re.finditer("</strong>", type_link)][1][0]
        title_stickers = type_link[start_name:end_name]
        found += 's'
        return title_stickers, found
    
    
def get_link(link, output, parser_type, print):
    i = 0
    while i < 5:
        try:
            title = None
            description = None
            members = None
            title_stickers = None
            bot_dict = None
            found = ''
            if '1' in parser_type or '2' in parser_type or '3' in parser_type or '4' in parser_type:
                url = 'https://t.me/' + link        #getting data from link
                r = requests.get(url, stream=True)  
                soup = bs4.BeautifulSoup(r.text, "html.parser") 
                type_link = str(soup.find_all('a', class_="tgme_action_button_new"))
                members_str = str(soup.find_all('div', class_="tgme_page_extra"))
            
                if '1' in parser_type or '2' in parser_type:
                    if 'Preview channel' in type_link:      #check for channel

                        members_int = re.findall(r'\d+', members_str)
                        members = ''
                        members = members.join(members_int)
                        try:
                            title = str(soup.find('div', class_="tgme_page_title").text)[1:-1].replace(';', ':')
                            try:
                                description = str(soup.find('div', class_="tgme_page_description").text).replace(';', ':')
                            except:
                                description = 'None'
                        except:
                            title = 'None'
                            description = 'None'
                        if members == '':
                            members = '0'
                        found += 'c'
                        
                if found == '':
                    if '1' in parser_type or '3' in parser_type:    
                        if 'Preview channel' not in type_link and 'members' in members_str:       #check for group
              
                            members_str = members_str.split(',')[0]
                            members_int = re.findall(r'\d+', members_str)
                            members = ''
                            members = members.join(members_int)
                            try:
                                title = str(soup.find('div', class_="tgme_page_title").text)[:-1].replace(';', ':')
                                try:
                                    description = str(soup.find('div', class_="tgme_page_description").text).replace(';', ':')
                                except:
                                    description = 'None'
                            except:
                                title = 'None'
                                description = 'None'
                            if members == '':
                                members = '0'
                            found += 'g'
                            
                if found == '':        
                    if '1' in parser_type or '4' in parser_type:    
                        if 'tgme_action_button_new' in type_link and 'member' not in members_str and 'Send Message' in type_link:
                            # if '1' in output or '2' in output:
                            #     print('Try: ' + link + ', result: New User')
                            try:
                                title = str(soup.find('div', class_="tgme_page_title").text)[:-1].replace(';', ':')
                                try:
                                    description = str(soup.find('div', class_="tgme_page_description").text).replace(';', ':')
                                except:
                                    description = 'None'
                            except:
                                title = 'None'
                                description = 'None'
                            found += 'u'
                
            if '1' in parser_type or '5' in parser_type:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(stickers_parser, link, found)
                    title_stickers, found = future.result()
            
            if '1' in parser_type or '6' in parser_type:
                bot_links = [link + '_bot', link + 'bot']
                i = 0
                bot_dict = dict()
                for link_bot in bot_links:
                    url_bot = 'https://t.me/' + link_bot
                    r_bot = requests.get(url_bot, stream=True)  
                    soup_bot = bs4.BeautifulSoup(r_bot.text, "html.parser") 
                    type_link = soup_bot.find_all('div', class_="tgme_page_extra")
                    if type_link != []:
                        title_bot = soup_bot.find('div', class_='tgme_page_title').text
                        try:
                            description_bot = soup_bot.find('div', class_='tgme_page_description').text
                        except:
                            description_bot = None
                        bot_dict['title_bot' + str(i)] = title_bot
                        bot_dict['description_bot' + str(i)] = description_bot
                        found += 'b' + str(i)
                    i += 1
            Thread(target = telegram_parser, args = (link, found, title, description, members, title_stickers, bot_dict)).start()
            if '1' in output or '2' in output:
                if '1' in output:
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
                        if 'b' in found:
                            mess += 'Bot, '
                    else:
                        mess = 'False'
                    print('Try: ' + link + ', result: ' + mess)

                if '2' in output:
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
                        if 'b' in found:
                            mess += 'Bot, '
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
            
def get_fast_link(link, output, parser_type, print):
    i = 0
    while i < 5:
        try:
            found = ''
            if '1' in parser_type or '2' in parser_type or '3' in parser_type or '4' in parser_type:
                url = 'https://t.me/' + link        #getting data from link
                r = requests.get(url, stream=True)  
                soup = bs4.BeautifulSoup(r.text, "html.parser") 
                type_link = str(soup.find_all('a', class_="tgme_action_button_new"))
                members_str = str(soup.find_all('div', class_="tgme_page_extra"))
            
                if '1' in parser_type or '2' in parser_type:
                    if 'Preview channel' in type_link:      #check for channel
                        found += 'c'
                        
                if found == '':
                    if '1' in parser_type or '3' in parser_type:    
                        if 'Preview channel' not in type_link and 'members' in members_str:       #check for group
                            found += 'g'
                            
                if found == '':        
                    if '1' in parser_type or '4' in parser_type:    
                        if 'tgme_action_button_new' in type_link and 'member' not in members_str and 'Send Message' in type_link:
                            found += 'u'
                
            if '1' in parser_type or '5' in parser_type:
                url_stickers = 'https://t.me/addstickers/' + link        #getting data from link
                r_stickers = requests.get(url_stickers, stream=True)  
                soup_stickers = bs4.BeautifulSoup(r_stickers.text, "html.parser") 
                type_link = str(soup_stickers.find_all('div', class_="tgme_page_description")).replace(u'\xa0', ' ').replace(';', ':')
                if re.search('Sticker Set', type_link):      #check for channel
                    pass 
                else:
                    found += 's'
            
            if '1' in parser_type or '6' in parser_type:
                bot_links = [link + '_bot', link + 'bot']
                i = 0
                for link_bot in bot_links:
                    url_bot = 'https://t.me/' + link_bot
                    r_bot = requests.get(url_bot, stream=True)  
                    soup_bot = bs4.BeautifulSoup(r_bot.text, "html.parser") 
                    type_link = soup_bot.find_all('div', class_="tgme_page_extra")
                    if type_link != []:
                        found += 'b' + str(i)
                    i += 1
           
            Thread(target = telegram_parser_fast, args = (link, found)).start()
            if '1' in output or '2' in output:
                if '1' in output:
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
                        if 'b' in found:
                            mess += 'Bot, '
                    else:
                        mess = 'False'
                    print('Try: ' + link + ', result: ' + mess)

                if '2' in output:
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
                        if 'b' in found:
                            mess += 'Bot, '
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