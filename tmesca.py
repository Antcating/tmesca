#! /usr/bin/env python3
from tmescalib.config import Config
from tmescalib.generators import get_generator

last_link = None

def start():
    config = Config(True)
    links = get_generator(config)
    for link in links:
        last_link = link
        print(link)

if __name__ == '__main__':
    start()