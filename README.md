<h1 align="center"><img src="logo.png" alt="tmesca" width="800"/></h1>

[README на русском](README_ru.md)

## What is it?
**tmesca** is a Telegram public entity scanner by parsing the contents of short links to `t.me`. The principle is extremely simple:
1. Generating a link to `t.me`
2. Download its contents
3. We analyze and determine what it is (user / channel / stickers, etc.)
4. We save information to the desired database based on the type of entity

Therefore **tmesca** doesn't require a Telegram account and doesn't depend on the Telegram API.

## Main features

1. Various link generation types:
   * Linear search - generates all links with a certain length. In other words, bruteforce.
   * Random search - generates random links from 5 to 32 characters long.
   <!-- * Mutation search - input word and script creates mutations of this word and check all possibilities.  -->
2. Parse content types:
   * Channels
   * Group
   * Users
   * Sticker Packs
   * Bots
3. Output to Telegram on the channel. 
4. Turbo mode - can be toggled to speed up parsing. 

## Known Issues
The current implementation (especially in turbo mode) doesn't consider the restrictions 300 requests per minute to `t.me` and may skip existing links.

## Installation and Run
You will need git, python3 and pip, and pipenv for the second method.

### Pure python
This method is recommended for beginners. Just run these commands in the terminal.
```bash
git clone https://github.com/Antcating/telegram_parser.git
cd telegram_parser/
pip install -r requirements.txt
python3 telegram_parser/console.py
```

### pipenv
A way for the advanced. This method assumes that you know what you are doing.
```bash
git clone https://github.com/Antcating/telegram_parser.git
cd telegram_parser/
pip install -r requirements.txt
python3 telegram_parser/console.py
```

## Telegram Output
If you want to use Telegram output: <br />
Before the first run, you **have to** change configuration file `telegram.ini`:
```
[Telegram]
user_id = id here
tg_token = bot token here
```
##### Instruction
- Create Telegram bot using [BotFather](https://t.me/BotFather) and get Telegram Bot Token.
- Get your Telegram account id. You can get it using [this bot](https://t.me/userinfobot). 
- In the config file `telegram.ini` paste Telegram Bot Token to the `tg_token` row, and id into `user_id` row.   
- Hooray! Everything ready. Enjoy!

### Requirements and thanks 
* [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/)
* [Requests](https://docs.python-requests.org/en/master/)
* [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
