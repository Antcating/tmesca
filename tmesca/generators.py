import random
import string

def get_generator(config):
    type_ = config.generator['type']
    if type_ == 'linear':
        return linear_addresses(config.session['seed'])
    elif type_ == 'random':
        return random_addresses()
    raise NotImplementedError(f'Generator {type_} not implemented')

ALPHABET_FIRST = string.ascii_lowercase
ALPHABET_LAST = ALPHABET_FIRST + string.digits
ALPHABET = ALPHABET_LAST + '_'


def random_addresses():
    while True:
        len_link = random.randint(5, 32)
        link = random.choices(ALPHABET_FIRST)
        link += random.choices(ALPHABET, k=len_link - 2)
        link += random.choices(ALPHABET_LAST)
        s_link = ''.join(link)
        if '__' in s_link:
            continue 
        yield s_link


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
