import random, string, itertools
from print_handler import print_func
import string

ALPHABET_FIRST = string.ascii_lowercase
ALPHABET_LAST = ALPHABET_FIRST + string.digits
ALPHABET = ALPHABET_LAST + '_'

def random_addresses():
    while True:
        len_link = random.randint(5, 32)
        link = random.choices(ALPHABET_FIRST)
        link += random.choices(ALPHABET, k=len_link - 2)
        link += random.choices(ALPHABET_LAST)
        yield ''.join(link)


def linear_addresses(seed, first=True):
    if len(seed) == 1:
        for letter in letters(ALPHABET_LAST, seed[0]):
            yield letter
    else:
        if first:
            alphabet = ALPHABET_FIRST
        else:
            alphabet = ALPHABET
        
        for link in linear_addresses(seed[1:], False):
            yield seed[0] + link
        
        new_seed = 'a' * (len(seed) - 1)
        for letter in letters(alphabet, seed[0], 1):
            for link in linear_addresses(new_seed, False):
                yield letter + link


def letters(alphabet, start='a', shift=0):
    position = alphabet.index(start)
    for letter in alphabet[position+shift:]:
        yield letter

# def mutation_address_generator(link):
#     mutated_array = []
#     replacements = """
# a=4
# b=6
# e=3
# f=8
# g=9
# i=1
# l=1
# o=0
# s=5
# t=7
# z=2
# """
#     try:
#         open('mutated', 'r').read()
#
#     except FileNotFoundError:
#         mutated_replacement_set = set()
#         mutated_array = []
#         link = [link]
#         mutations = ['_', 'xxx']
#         for number_of_connected_mutations in range(1, len(mutations) + 2):
#             for mutation_tuple in itertools.permutations(link + mutations, number_of_connected_mutations):
#                 mutation_word = ''.join(mutation_tuple)
#                 if link[0] in mutation_word or link[0] == mutation_word:
#                     if len(mutation_word) > 4 and len(mutation_word) < 33:
#                         if mutation_word[0] not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_'] and \
#                                 mutation_word[-1] not in ['_']:
#                             mutated_replacement_set.add(mutation_word)
#
#         d = {c: [c] for c in string.printable}
#         for line in replacements.strip().split("\n"):
#             c, replacement = line.split("=")
#             d[c].append(replacement)
#
#         for link in mutated_replacement_set:
#             for letters in itertools.product(*[d[c] for c in link]):
#                 mutated_address = "".join(letters)
#                 if mutated_address[0] not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_']:
#                     mutated_array.append(mutated_address)
#         return mutated_array
