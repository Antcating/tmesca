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

## Restrictions
`t.me` only allows 300 requests per minute from one address.

## Installation and Run
You will need git, python3 and pip, and pipenv for the second method.

### Pure python
This method is recommended for beginners. Just run these commands in the terminal.
```bash
git clone https://github.com/Antcating/tmesca.git
cd tmesca/
pip install -r requirements.txt
python3 -m tmesca
```

### pipenv
A way for the advanced. This method assumes that you know what you are doing.
```bash
git clone https://github.com/Antcating/tmesca.git
cd tmesca/
pipenv install
pipenv run tmesca
```

## Configuration
**tmesca** does not require any default configuration and will ask for all necessary settings at startup. However, for regular launches, it may be more convenient to configure for yourself. For a basic configuration, just copy the file `tmesca.example.yml` to` tmesca.yml`. You can find a detailed description of all fields in the same file.

### Difference between `soup` and` lighting`
The soup parser runs on top of Beautiful Soup and lxml, and the lighting parser uses simple string comparisons. Accordingly, `soup` works more accurately, but` lighting` is ~30% faster. It is recommended to use `lighting` with` link` mode, and `soup` with` full` mode.

## Telegram Output
- Create Telegram bot using [BotFather](https://t.me/BotFather) and get Telegram Bot Token.
- Get your Telegram account id. You can get it using [this bot](https://t.me/userinfobot). 
- Create config if not already. You can comment out everything you don't need.
- In the config, insert the Bot Token Telegram obtained earlier into the `bot_token` line, and the id into the` user_id` line.
- Hooray! Everything ready. Enjoy!

### Requirements and thanks 
* [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/)
* [Requests](https://docs.python-requests.org/en/master/)
* [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
