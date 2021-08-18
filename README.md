# <p align="center">Total Telegram GUI/Console Parser
# <p align="center"><img src="icon.png" alt="drawing" width="200"/>
Script parse telegram links and sort them to channel/group/user/sticker pack/bot database.


Script doesn't require Telegram account or any usage of Telegram API. Whole algorithm based on Telegram website and site scrapper BeautifulSoup4, so that this script can work without Telegram API delay.

---

Read on [Русском](https://github.com/Antcating/telegram_parser/blob/main/README_ru.md)  [English](https://github.com/Antcating/telegram_parser/blob/main/README_ru.md)

### Main features


1. Parse types:
   * Linear search - choose the length of the link and parse all links, that are in this range.
   * Random search - creates random link from 5 to 32 symbols and check it.
   * Mutation search - input word and script creates mutations of this word and check all possibilities. 
2. Parse content types:
   * Channels
   * Group
   * Users
   * Sticker Packs
   * Bots
   * All possible intersections between the above types
3. Output to Telegram on the channel. 
4. Turbo mode - can be toggled to speed up parsing. 

---

### Config

#### Initial Config
Before the first run, you **have to** change configuration file `telegram.ini`:
```
[Telegram]
user_id = id here
tg_token = bot token here
```
* Telegram Parser uses Telegram Bots to control Parser, so you will **have to** go to [BotFather](https://t.me/BotFather) and create bot using its instructions. After creating bot, BotFather will return token to access the HTTP API. You will have to copy-paste it to the configuration file on the `tg_token` row.
* Bot sends founds in user chat. So, you have to get your Telegram id. You can to it, for example, using [this bot](https://t.me/userinfobot). Your id you paste to the config on the `user_id` row. <br />

---
  
Whole other configuration, such as:
* Parse type
* Turbo mode
* Parse content type
* Subsettings for some of types
* etc., <br />
is making on the start of the script.


#### Telegram Output
To make Telegram output you have to: <br />
- Create Telegram bot using [BotFather](https://t.me/BotFather) and get Telegram Bot Token.
- Create **public** channel (or, if you know, how to get private channel ID, you can use it). 
- Add bot, you just created, to the channel with permission to post/read messages. 
- In the program choose Telegram output and paste in the corresponding line Bot Token and Channel Link (if you already done it, just press Skip).   
- Hooray! Everything ready. Enjoy!


---

### Installation and Run
Using console:<br />
```
git clone https://github.com/Antcating/telegram_parser.git
cd telegram_parser/telegram_parser/
python3 console.py
```
#### Warning!
Also, make sure, that all the requirements are installed:
```
cd telegram_parser
pip3 install -r requirements.txt
```
If you have already downloaded older version of the program in the past, you can delete and get all over the instructions or just update the existing folder:
```
cd telegram_parser
git pull
```

---

### Usage
From the folder in which you cloned/downloaded the script you have to go to subfolder called telegram_parser, and run through the console _python3 gui.py_ or _python3 console.py_

---

### Requirements and thanks 
* [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/)
* [Requests](https://docs.python-requests.org/en/master/)
* [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI)
* [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
