import requests, bs4, time, re, sys, random, csv
from database_check import database_check
from link_processor import get_link

database_check()

def start_link():
    n_letters = input('How many letters in the link might be? ')
    start_point = 'a' + '1'*int(n_letters)
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
                    
            get_link(link, output)
            
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