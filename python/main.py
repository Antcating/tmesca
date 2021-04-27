import requests, bs4, time, re, sys, random
import csv

try:                                                                    # checking existing of the telegram_parser.csv file
    csvfile_read = open('telegram_parser.csv', 'r').close()
    
except:
    csvfile = open('telegram_parser.csv', 'a+')
    with open('telegram_parser.csv','a',newline='') as f:
        csv_writer=csv.writer(f)
        csv_writer.writerow(['adress', 'title', 'description', 'members'])
        
try:                                                                    # checking existing of the group_telegram_parser.csv file
    csvfile_read = open('group_telegram_parser.csv', 'r').close()
except:
    csvfile = open('group_telegram_parser.csv', 'a+')
    with open('group_telegram_parser.csv','a',newline='') as f:
        csv_writer=csv.writer(f)
        csv_writer.writerow(['adress', 'title', 'description', 'members'])

def start_link():
    n_letters = input('How many letters in the link might be? ')
    start_point = 'a' + '1'*(n_letters)
    open('last_link', 'w').write(start_point)
    
try:                                    # LINK Checking
    start_point = open('last_link').read()
except:
    start_link()
rand_mode = input('Do you want to use random links mode(y/n): ')[0].lower()
if rand_mode != 'y':
    change_start = input('Do you want to change number of letters in link(y/n): ')[0].lower()
    if change_start == 'y':
        start_link()
turbo_mode = input('Turn on turbo mod(y/n): ')                     # work mode with/out delay
output = input('Show output(y/n): ')[0].lower()


def main(mode, output, rand_mode):
    print('Parser is started!')
    alphabet = ['1', '2', '3','4' , '5', '6', '7', '8', '9', '0', '_']
    for letter in range(97,123):            #all letters except first alphabet
        alphabet.append(chr(letter))
        
    alphabet1 = []                          #first letter alphabet
    for letter in range(97,123):
        alphabet1.append(chr(letter))
    

    start_point = open('last_link').read()
         # LINK GENERATION
    link_index_array = []
    for i in range(len(start_point)): 
        if i == 0:        
            link_index_array.append(alphabet1.index(start_point[i])) 
        elif i == len(start_point)-1:
            link_index_array.append(alphabet.index(start_point[i])+1)
        else:
            link_index_array.append(alphabet.index(start_point[i]))
    try:
        while True:
            if rand_mode == 'y':
                len_link = random.randint(5, 32)
                link = ''
                for i in range(len_link):
                    if i == 0:
                        link += alphabet1[random.randint(0, len(alphabet1)-1)]
                    else:
                        link += alphabet[random.randint(0, len(alphabet)-1)]
            
            else:
                link = ''
                for i in range(len(link_index_array)):
                    if i == 0:  
                        link += str(alphabet1[link_index_array[i]])
                    else:
                        link += str(alphabet[link_index_array[i]])
    
                link_index_array[-1] += 1
                for i in range(len(link_index_array)-1, -1, -1):
                    if i != 0:
                        if link_index_array[i] == len(alphabet):
                            link_index_array[i] = 0
                            link_index_array[i-1] += 1
                    else:
                        if link_index_array[0] == len(alphabet1):
                            break
                    
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
                
                
            open('last_link', 'w').write(link)
            if turbo_mode != 'y':
                time.sleep(1.5)
            else:
                continue
    except ConnectionError:         #exceptions
        print('Waiting for Internet')
        time.sleep(10)
    except KeyboardInterrupt:
        open('last_link', 'w').write(link)
        sys.exit(0)
    
main(turbo_mode, output, rand_mode)