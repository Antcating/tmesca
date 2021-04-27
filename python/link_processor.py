import requests, bs4, re, csv

def get_link(link, output):
    url = 'https://t.me/' + link        #getting data from link
    r = requests.get(url, stream=True)  
    soup = bs4.BeautifulSoup(r.text, "html.parser") 
    type_link = str(soup.find_all('a', class_="tgme_action_button_new"))
    members_str = str(soup.find_all('div', class_="tgme_page_extra"))
    
    
    if 'Preview channel' in type_link:      #check for channel
        if output == 'y':
            print('Try: ' + link + ', result: New Channel')
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
        with open('telegram_parser.csv','a',newline='') as f:
            csv_writer=csv.writer(f)
            csv_writer.writerow([link, title, description, members])
    
    elif 'Preview channel' not in type_link and 'members' in members_str:       #check for group
        if output == 'y':
            print('Try: ' + link + ', result: New Group')
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
    else:
        if output == 'y':
            print('Try: ' + link + ', result: False')