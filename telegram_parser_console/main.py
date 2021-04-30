import time, sys, os
from database_check import database_check
from link_processor import get_link
from link_generator import alphabets_generator, random_address_generator, linear_address_generator, last_link_read_linear_address, mutation_address_generator


def program_exit(link, work_mode):
    if work_mode == '1':            # 1 = linear
        print('Saving last linear link position')
        open('last_link', 'w').write(link)
    # if work_mode == '3':
    #     print('Mutation variations of the link ended')
    print('Script stoped')
    sys.exit(0)    

def start_link():
    n_letters = input('How many letters in the link might be (at least 5): ')
    start_point = 'a' + '1'*(int(n_letters)-1)
    open('last_link', 'w').write(start_point)


database_check()
    

def main():
    parser_type = input('''What type of content do you want to parse (input several numbers, if you want to parse any combination of the possible content): 
 1 - All (Groups/Channel/Users
 2 - Channels
 3 - Groups
 4 - Users
Your choise: ''')[:2].lower()
    work_mode = input('''What type of parsing you want to use:
 1 - Linear parsing
 2 - Random parsing 
 3 - Mutation parsing 
Your choise: ''')[0].lower()
    turbo_mode = input('Turn on turbo mod(y/n): ')[0].lower()                   # work mode with/out delay
    output = input('''What type of output do you want: 
 1 - All output (not False will be only the content, that was choosed to parse)
 2 - If something found
 3 - No output
Your choise: ''')[0].lower()
    
    alphabet, alphabet1 = alphabets_generator()
    if work_mode == '1':
        try:                                    # LINK Checking
            open('last_link').read()
            change_start = input('Do you want to change number of letters in link(y/n): ')[0].lower()
            if change_start == 'y':
                start_link()
        except:
            print('Initial setup!')
            start_link()
        linear_letter_link_ids_array = last_link_read_linear_address(alphabet, alphabet1)
    
    if work_mode == '3':
        try:
            os.remove('mutated')
        except:
            pass
        mutated_initial_link =  input('Input initial word to mutate (length of the word is greater than 5 letters): ').lower()
        mutated_array = mutation_address_generator(mutated_initial_link)
        total_mutated_rows = len(mutated_array)
        print('Total mutation created: ',total_mutated_rows)
        mutated_word_id = 0
    try:
        print('Parser is started!')
        while True:
            if work_mode =='1':             # 1 = linear
                link = linear_address_generator(alphabet, alphabet1, linear_letter_link_ids_array)
                open('last_link', 'w').write(link)
            elif work_mode == '2':          # 2 = random
                link = random_address_generator(alphabet, alphabet1)
            elif work_mode == '3':          # 3 = mutation
                if total_mutated_rows > mutated_word_id +1:
                    link = mutated_array[mutated_word_id]
                    mutated_word_id += 1
                else: 
                    program_exit(link, work_mode)
            url_get_status = get_link(link, output, parser_type)
            if url_get_status == 'connection_error':
                program_exit(link, work_mode)
            
            if turbo_mode != 'y':
                time.sleep(1.5)
            else:
                continue
    except KeyboardInterrupt:
        if work_mode == '3':
            print('Mutation checking keyboard interupted')
        program_exit(link, work_mode)
  

main()