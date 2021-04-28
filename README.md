# <p align="center">Telegram Group/Channel Parser
# <img src="icon.png" alt="drawing" width="200"/>
Telegram Parser
 Script parse telegram links and sort them to channel/group database.


Script doesn't require Telegram account or any usage of Telegram API. Whole algorithm based on Telegram website and site scrapper BeautifulSoup4, so that this script can work without Telegram API delay.

---

### Main features
1. Parse types:
    * Linear search - choose the length of the link and parse all links, that are in this range.
    * Random search - creates random link from 5 to 32 symbols and check it.
    * Mutation search - input word and script creates mutations of this word and check all possibilities.
2. Parse content types:
    * Channels
    * Group
    * Users
    * All possible intersections between the above types 
3. Turbo mode - can be toggled to speed up parsing. 

---

### Installation and run
Using console:
```
git clone https://github.com/Antcating/telegram_parser.git
cd telegram_parser/main/
python3 main.py
```
Also, make sure, that all the requirements are installed:
```
cd telegram_parser
pip3 install -r requirements.txt
```
---

### Config

#### Initial Config
Whole configuration, such as:
* Parse type
* Turbo mode
* Parse content type
* Subsettings for some of types
* etc.,
is making on the start of the script.

---

### Usage
From the folder in which you cloned/downloaded the script you have to go to subfolder called _python_, and run throw the console _python3 main.py_

---

### Requirements and thanks 
* [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/)
* [Requests](https://docs.python-requests.org/en/master/)
