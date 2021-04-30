import random, string, itertools

def alphabets_generator():
    alphabet = ['1', '2', '3','4' , '5', '6', '7', '8', '9', '0', '_']
    for letter in range(97,123):            #all letters except first alphabet
        alphabet.append(chr(letter))
        
    alphabet1 = []                          #first letter alphabet
    for letter in range(97,123):
        alphabet1.append(chr(letter))
    return alphabet, alphabet1

def random_address_generator(alphabet, alphabet1):
    len_link = random.randint(5, 32)
    link = ''
    for i in range(len_link):
        if i == 0:
            link += alphabet1[random.randint(0, len(alphabet1)-1)]
        else:
            link += alphabet[random.randint(0, len(alphabet)-1)]
    return link

def last_link_read_linear_address(alphabet, alphabet1):
    start_point = open('last_link').read()
    linear_letter_link_ids_array = []
    for i in range(len(start_point)): 
        if i == 0:        
            linear_letter_link_ids_array.append(alphabet1.index(start_point[i])) 
        elif i == len(start_point)-1:
            linear_letter_link_ids_array.append(alphabet.index(start_point[i])+1)
        else:
            linear_letter_link_ids_array.append(alphabet.index(start_point[i]))
    return linear_letter_link_ids_array

def linear_address_generator(alphabet, alphabet1, linear_letter_link_ids_array):
    link = ''
    for i in range(len(linear_letter_link_ids_array)):
        if i == 0:  
            link += str(alphabet1[linear_letter_link_ids_array[i]])
        else:
            link += str(alphabet[linear_letter_link_ids_array[i]])

    linear_letter_link_ids_array[-1] += 1
    for i in range(len(linear_letter_link_ids_array)-1, -1, -1):
        if i != 0:
            if linear_letter_link_ids_array[i] == len(alphabet):
                linear_letter_link_ids_array[i] = 0
                linear_letter_link_ids_array[i-1] += 1
        else:
            if linear_letter_link_ids_array[0] == len(alphabet1):
                print('The end of this linear range. Exiting the program.')
                break
    return link

def mutation_address_generator(link):
    mutated_array = []
    replacements = """
a=4
b=6
e=3
f=8
g=9
i=1
l=1
o=0
s=5
t=7
z=2
"""
    try:
        open('mutated', 'r').read()
        
    except FileNotFoundError:
        mutated_replacement_set = set()
        mutated_array = []
        link = ['telegram']
        mutations = ['_', 'xxx']
        for number_of_connected_mutations in range(1, len(mutations) + 2):
            for mutation_tuple in itertools.permutations(link + mutations, number_of_connected_mutations):
                mutation_word = ''.join(mutation_tuple)
                if link[0] in mutation_word or link[0] == mutation_word:
                    if len(mutation_word) > 4 and len(mutation_word) < 33:
                        if mutation_word[0] not in ['0','1', '2', '3','4', '5', '6', '7', '8', '9', '_'] and mutation_word[-1] not in ['_']:
                            mutated_replacement_set.add(mutation_word)
        
        d = {c:[c] for c in string.printable}
        for line in replacements.strip().split("\n"):
            c, replacement = line.split("=")
            d[c].append(replacement)
        
        for link in mutated_replacement_set:
            for letters in itertools.product(*[d[c] for c in link]):
                mutated_address = "".join(letters)
                if mutated_address[0] not in ['0','1', '2', '3','4', '5', '6', '7', '8', '9', '_']:
                    mutated_array.append(mutated_address)
        return mutated_array
