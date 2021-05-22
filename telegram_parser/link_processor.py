import requests, bs4, re, csv, time, os, cchardet, lxml
from threading import Thread
import concurrent.futures


def telegram_parser_open():
    try:
        channel_db = open('output/channel_telegram_parser.csv','a',newline='')
        group_db = open('output/group_telegram_parser.csv','a',newline='')
        user_db = open('output/user_telegram_parser.csv','a',newline='')
        sticker_db = open('output/stickers_telegram_parser.csv','a',newline='') 
        bot0_db = open('output/bots_telegram_parser.csv','a',newline='') 
        bot1_db = open('output/bots_telegram_parser.csv','a',newline='') 
    except FileNotFoundError:
        os.mkdir('output')
        telegram_parser_open()
    return channel_db, group_db, user_db, sticker_db, bot0_db, bot1_db


with open('output/channel_telegram_parser.csv','a',newline='') as channel_db:
    def telegram_parser(channel_db, 
                        group_db,
                        user_db,
                        sticker_db,
                        bot0_db,
                        bot1_db,
                        
                        link, 
                        found, 
                        title, 
                        description, 
                        members, 
                        title_stickers, 
                        bot_dict
                        ):
        if 'c' in found:
            csv.writer(channel_db).writerow([link, title, description, members])
        elif 'g' in found:
            csv.writer(group_db).writerow([link, title, description, members]) 
        elif 'u' in found:
            csv.writer(user_db).writerow([link, title, description]) 
        if 's' in found:
            csv.writer(sticker_db).writerow([link, title_stickers]) 
        if 'b0' in found:
            csv.writer(bot0_db).writerow([link + '_bot', bot_dict['title_bot0'], bot_dict['description_bot0']]) 
        if 'b1' in found:
            csv.writer(bot1_db).writerow([link + 'bot', bot_dict['title_bot1'], bot_dict['description_bot1']]) 

def fast_telegram_parser_open():
    try:
        channel_fast_db = open('output/channel_telegram_parser_fast.csv','a',newline='')
        group_fast_db = open('output/group_telegram_parser_fast.csv','a',newline='')
        user_fast_db = open('output/user_telegram_parser_fast.csv','a',newline='')
        sticker_fast_db = open('output/stickers_telegram_parser_fast.csv','a',newline='') 
        bot0_fast_db = open('output/bots_telegram_parser_fast.csv','a',newline='') 
        bot1_fast_db = open('output/bots_telegram_parser_fast.csv','a',newline='') 
    except FileNotFoundError:
        os.mkdir('output')
        fast_telegram_parser_open()
    return channel_fast_db, group_fast_db, user_fast_db, sticker_fast_db, bot0_fast_db, bot1_fast_db


with open('output/channel_telegram_parser.csv','a',newline='') as channel_fast_db:
    def fast_telegram_parser(
                        channel_fast_db, 
                        group_fast_db,
                        user_fast_db,
                        sticker_fast_db,
                        bot0_fast_db,
                        bot1_fast_db,
                        
                        link, 
                        found, 
                        ):
        if 'c' in found:
            csv.writer(channel_fast_db).writerow([link])
        elif 'g' in found:
            csv.writer(group_fast_db).writerow([link]) 
        elif 'u' in found:
            csv.writer(user_fast_db).writerow([link]) 
        if 's' in found:
            csv.writer(sticker_fast_db).writerow([link]) 
        if 'b0' in found:
            csv.writer(bot0_fast_db).writerow([link + '_bot']) 
        if 'b1' in found:
            csv.writer(bot1_fast_db).writerow([link + 'bot']) 
  
    
def channel_group_user_get(link, found, parser_type):
    title = None
    description = None
    members = None
    url = 'https://t.me/' + link        #getting data from link
    s = requests.Session()
    r = s.get(url, stream=True)  
    soup = bs4.BeautifulSoup(r.text, "lxml", ) 
    type_link = str(soup.find_all('a', class_="tgme_action_button_new"))
    members_str = str(soup.find_all('div', class_="tgme_page_extra"))

    try:
        title = str(soup.find('div', class_="tgme_page_title").text)[1:-1].replace(';', ':')
        try:
            description = str(soup.find('div', class_="tgme_page_description").text).replace(';', ':')
        except:
            pass
    except AttributeError:
        return title, description, members, found
        
    if any(parser_mode in parser_type for parser_mode in ['1', '2']):
        if re.search('Preview channel', type_link):      #check for channel
            members_int = re.findall(r'\d+', members_str)
            members = ''
            members = members.join(members_int)
            if members == '':
                members = '0'
            found += 'c,' 
            return title, description, members, found
    if found == '':
        if any(parser_mode in parser_type for parser_mode in ['1', '3']):
            if 'Preview channel' not in type_link and 'members' in members_str:       #check for group
                members_str = members_str.split(',')[0]
                members_int = re.findall(r'\d+', members_str)
                members = ''
                members = members.join(members_int)
                if members == '':
                    members = '0'
                found += 'g,'
                return title, description, members, found
                
    if found == '':        
        if any(parser_mode in parser_type for parser_mode in ['1', '4']):  
            if 'tgme_action_button_new' in type_link and 'member' not in members_str and 'Send Message' in type_link:
                members = None
                found += 'u,'
                return title, description, members, found
    return title, description, members, found

def stickers_get(link, found):
    url_stickers = 'https://t.me/addstickers/' + link        #getting data from link
    r_stickers = requests.get(url_stickers, stream=True)  
    soup_stickers = bs4.BeautifulSoup(r_stickers.text, "lxml", ) 
    type_link = str(soup_stickers.find_all('div', class_="tgme_page_description")).replace(u'\xa0', ' ').replace(';', ':')
    if re.search('Sticker Set', type_link):      
        return None, found
    else:
        start_name = [(m.start(0), m.end(0)) for m in re.finditer("<strong>", type_link)][1][1]
        end_name = [(m.start(0), m.end(0)) for m in re.finditer("</strong>", type_link)][1][0]
        title_stickers = type_link[start_name:end_name]
        found += 's,'
        return title_stickers, found

       
def bot_get(link, found):
    bot_links = [link + '_bot', link + 'bot']
    i = 0
    bot_dict = dict()
    for link_bot in bot_links:
        url_bot = 'https://t.me/' + link_bot
        r_bot = requests.get(url_bot, stream=True)  
        soup_bot = bs4.BeautifulSoup(r_bot.text, "lxml", ) 
        type_link = soup_bot.find_all('div', class_="tgme_page_extra")
        if type_link != []:
            title_bot = soup_bot.find('div', class_='tgme_page_title').text
            try:
                description_bot = soup_bot.find('div', class_='tgme_page_description').text
            except:
                description_bot = None
            bot_dict['title_bot' + str(i)] = title_bot
            bot_dict['description_bot' + str(i)] = description_bot
            found += 'b' + str(i) + ','
        i += 1
    return bot_dict, found


def output_func(found, link, output, print):
    output_dict = {
    'c':'Channel, ',
    'g': 'Group, ',
    'u': 'User, ',
    's': 'Sticker Pack, ',
    'b0': 'Bot, ',
    'b1': 'Bot, ',
    }
    if '1' in output or '2' in output:
        if found != '':
            mess = ''
            for found_item in found.split(','):
                if found_item != '':
                    mess += output_dict[found_item]
        else:
            mess = 'False'
        if '2' in output:
            if mess == 'False':
                return
        print('Try: ' + link + ', result: ' + mess)
        

def get_link(link, output, parser_type, print, channel_db, group_db, user_db, stickers_db, bot0_db, bot1_db):
    
    i = 0
    while i < 5:
        try:
            title = None
            description = None
            members = None
            title_stickers = None
            bot_dict = None
            found = ''
            if any(parser_mode in parser_type for parser_mode in ['1', '2', '3', '4', '5', '6']):
                with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
                    if any(parser_mode in parser_type for parser_mode in ['1', '2', '3', '4']):
                        channel_group_user_future = executor.submit(channel_group_user_get, link, found, parser_type)
                        title, description, members, found = channel_group_user_future.result()
                    if any(parser_mode in parser_type for parser_mode in ['1', '5']):
                        sticker_future = executor.submit(stickers_get, link, found)
                        title_stickers, found = sticker_future.result()
                    if any(parser_mode in parser_type for parser_mode in ['1', '6']):
                        bot_future = executor.submit(bot_get, link, found)
                        bot_dict, found = bot_future.result()

            Thread(target = telegram_parser, args = (   channel_db,
                                                        group_db, 
                                                        user_db,
                                                        stickers_db, 
                                                        bot0_db, 
                                                        bot1_db,
                
                                                        link, 
                                                        found, 
                                                        title, 
                                                        description, 
                                                        members, 
                                                        title_stickers, 
                                                        bot_dict
                                                        )).start()
            
            output_func(found, link, output, print)

            return
        except OSError:         #exceptions
            if i != 4:    
                print('No connection. Pause script')
            if i == 4:
                print('Connection error. Stop script.')
                return 'connection_error'
            i += 1
            time.sleep(10)
            
    
def fast_channel_group_user_get(link, found, parser_type):
    url = 'https://t.me/' + link        #getting data from link
    r = requests.get(url, stream=True)  
    soup = bs4.BeautifulSoup(r.text, "lxml", ) 
    type_link = str(soup.find_all('a', class_="tgme_action_button_new"))
    members_str = str(soup.find_all('div', class_="tgme_page_extra"))
    if any(parser_mode in parser_type for parser_mode in ['1', '2']):  
        if 'Preview channel' in type_link:      #check for channel
            found += 'c,'
            return found
    if found == '':
        if any(parser_mode in parser_type for parser_mode in ['1', '3']):  
            if 'Preview channel' not in type_link and 'members' in members_str:       #check for group
                found += 'g,'
                return found
    if found == '':        
        if any(parser_mode in parser_type for parser_mode in ['1', '4']):  
            if 'tgme_action_button_new' in type_link and 'member' not in members_str and 'Send Message' in type_link:
                found += 'u,'
                return found
    return found

def fast_stickers_get(link, found):
    url_stickers = 'https://t.me/addstickers/' + link        #getting data from link
    r_stickers = requests.get(url_stickers, stream=True)  
    soup_stickers = bs4.BeautifulSoup(r_stickers.text, "lxml", ) 
    type_link = str(soup_stickers.find_all('div', class_="tgme_page_description")).replace(u'\xa0', ' ').replace(';', ':')
    if re.search('Sticker Set', type_link):      #check for channel
        return found
    else:
        found += 's,'
        return found
       
def fast_bot_get(link, found):
    bot_links = [link + '_bot', link + 'bot']
    i = 0
    for link_bot in bot_links:
        url_bot = 'https://t.me/' + link_bot
        r_bot = requests.get(url_bot, stream=True)  
        soup_bot = bs4.BeautifulSoup(r_bot.text, "lxml", ) 
        type_link = soup_bot.find_all('div', class_="tgme_page_extra")
        if type_link != []:
            found += 'b' + str(i) + ','
        i += 1
    return found

def get_fast_link(link, output, parser_type, print, channel_fast_db, group_fast_db, user_fast_db, sticker_fast_db, bot0_fast_db, bot1_fast_db):
    i = 0
    while i < 5:
        try:
            found = ''
            if any(parser_mode in parser_type for parser_mode in ['1', '2', '3', '4', '5', '6']):
                with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
                    if any(parser_mode in parser_type for parser_mode in ['1', '2', '3', '4']):
                        channel_group_user_future = executor.submit(fast_channel_group_user_get, link, found, parser_type)
                        found = channel_group_user_future.result()
                    if any(parser_mode in parser_type for parser_mode in ['1', '5']):
                        sticker_future = executor.submit(fast_stickers_get, link, found)
                        found = sticker_future.result()
                    if any(parser_mode in parser_type for parser_mode in ['1', '6']):
                        bot_future = executor.submit(fast_bot_get, link, found)
                        found = bot_future.result()
           
            Thread(target = fast_telegram_parser,args =  (
                                                  channel_fast_db, 
                                                  group_fast_db, 
                                                  user_fast_db, 
                                                  sticker_fast_db, 
                                                  bot0_fast_db, 
                                                  bot1_fast_db, 
                                                  link, 
                                                  found, 
                                                  )).start()
            
            output_func(found, link, output, print)
                    
            return
        except OSError:         #exceptions
            if i != 4:    
                print('No connection. Pause script')
            if i == 4:
                print('Connection error. Stop script.')
                return 'connection_error'
            i += 1
            time.sleep(10)