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
