# <p align="center">pyTelegramBotAPI
Telegram Parser
 Script parse telegram links and sort them to channel/group database.


Script doesn't require Telegram account or any usage of Telegram API. Whole algorithm based on Telegram website and site scrapper BeautifulSoup4, so that this script can work without Telegram API delay.

### Installation and run
Using console:
```
git clone https://github.com/Antcating/telegram_parser.git
cd telegram_parcer/main/
python3 main.py
```


### Config

#### Initial Config
Whole configuration, such as:
* Random page mode
* Turbo mode
* Link generation length
* etc.
is making on the start of the script.

### Usage
From the folder in which you cloned/downloaded the script you have to go to subfolder called _python_, and run throw the console _python3 main.py_

### Requirements and thanks 
* [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/)
* [Requests](https://docs.python-requests.org/en/master/)