import re

import bs4
import requests


class Basic:
    def parse(self, link):
        if link['type'] == 'stickers':
            return self.parse_stickers(link['link'])
        if link['type'] == 'user':
            return self.parse_user(link['link'])
        if link['type'] == 'bot':
            return self.parse_bot(link['link'])
        raise NotImplementedError(f'Type {link["type"]} not implemented')

    def parse_user(self, link):
        url = 'https://t.me/' + link  # getting data from link
        r = requests.get(url, stream=True)
        soup = bs4.BeautifulSoup(r.text, "lxml", )
        type_link = str(soup.find_all('a', class_="tgme_action_button_new"))
        members_str = str(soup.find_all('div', class_="tgme_page_extra"))
        if 'Preview channel' in type_link:
            return {
                'type': 'channel',
                'link': url
            }
        if 'Preview channel' not in type_link and 'members' in members_str:  # check for group
            return {
                'type': 'group',
                'link': url
            }
        if 'tgme_action_button_new' in type_link and 'member' not in members_str and 'Send Message' in type_link:
            return {
                'type': 'user',
                'link': url
            }
        return None

    def parse_stickers(self, link):
        url_stickers = 'https://t.me/addstickers/' + link  # getting data from link
        r_stickers = requests.get(url_stickers, stream=True)
        soup_stickers = bs4.BeautifulSoup(r_stickers.text, "lxml", )
        type_link = str(soup_stickers.find_all('div', class_="tgme_page_description")).replace(u'\xa0', ' ').replace(';',
                                                                                                                     ':')
        if re.search('Sticker Set', type_link):  # check for channel
            return None
        return {
            'type': 'stickers',
            'link': url_stickers
        }

    def parse_bot(self, link):
        url_bot = 'https://t.me/' + link
        r_bot = requests.get(url_bot, stream=True)
        soup_bot = bs4.BeautifulSoup(r_bot.text, "lxml", )
        type_link = soup_bot.find_all('div', class_="tgme_page_extra")
        if type_link != []:
            return {
                'type': 'bot',
                'link': url_bot
            }
        return None


class FullInfo:
    def parse(self, link):
        if link['type'] == 'stickers':
            return self.parse_stickers(link['link'])
        if link['type'] == 'user':
            return self.parse_user(link['link'])
        if link['type'] == 'bot':
            return self.parse_bot(link['link'])
        raise NotImplementedError(f'Type {link["type"]} not implemented')

    def parse_user(self, link):
        title = None
        description = None
        members = None
        url = 'https://t.me/' + link  # getting data from link
        s = requests.Session()
        r = s.get(url, stream=True)
        soup = bs4.BeautifulSoup(r.text, "lxml", )
        type_link = str(soup.find_all('a', class_="tgme_action_button_new"))
        members_str = str(soup.find_all('div', class_="tgme_page_extra"))

        try:
            title = str(soup.find('div', class_="tgme_page_title").text)[
                1:-1].replace(';', ':')
            try:
                description = str(
                    soup.find('div', class_="tgme_page_description").text).replace(';', ':')
            except:
                pass
        except AttributeError:
            return None

        if re.search('Preview channel', type_link):  # check for channel
            members_int = re.findall(r'\d+', members_str)
            members = members.join(members_int)
            if members == '':
                members = '0'
            return {
                'type': 'channel',
                'link': url,
                'title': title,
                'description': description,
                'members': members
            }

        if 'Preview channel' not in type_link and 'members' in members_str:  # check for group
            members_str = members_str.split(',')[0]
            members_int = re.findall(r'\d+', members_str)
            members = members.join(members_int)
            if members == '':
                members = '0'
            return {
                'type': 'group',
                'link': url,
                'title': title,
                'description': description,
                'members': members
            }

        if 'tgme_action_button_new' in type_link and 'member' not in members_str and 'Send Message' in type_link:
            return {
                'type': 'user',
                'link': url,
                'title': title,
                'description': description
            }
        return None

    def parse_stickers(self, link):
        url_stickers = 'https://t.me/addstickers/' + link  # getting data from link
        r_stickers = requests.get(url_stickers, stream=True)
        soup_stickers = bs4.BeautifulSoup(r_stickers.text, "lxml", )
        type_link = str(soup_stickers.find_all('div', class_="tgme_page_description")).replace(u'\xa0', ' ').replace(';',
                                                                                                                     ':')
        if re.search('Sticker Set', type_link):
            return None

        start_name = [(m.start(0), m.end(0))
                      for m in re.finditer("<strong>", type_link)][1][1]
        end_name = [(m.start(0), m.end(0))
                    for m in re.finditer("</strong>", type_link)][1][0]
        title_stickers = type_link[start_name:end_name]
        return {
            'type': 'user',
            'link': url_stickers,
            'title': title_stickers
        }

    def parse_bot(self, link):
        url_bot = 'https://t.me/' + link
        r_bot = requests.get(url_bot, stream=True)
        soup_bot = bs4.BeautifulSoup(r_bot.text, "lxml", )
        type_link = soup_bot.find_all('div', class_="tgme_page_extra")
        if type_link != []:
            title_bot = soup_bot.find('div', class_='tgme_page_title').text
            try:
                description_bot = soup_bot.find(
                    'div', class_='tgme_page_description').text
            except:
                description_bot = None
            return {
                'type': 'bot',
                'link': url_bot,
                'title': title_bot,
                'description': description_bot
            }
        return None
