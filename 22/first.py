import sys # argv
import re


TOTAL_CARDS = 10007
card_index = 2019
with open(sys.argv[1]) as f:
    for line in f:
        line = line.strip()
        if line == 'deal into new stack':
            card_index = TOTAL_CARDS - card_index - 1
        elif m := re.fullmatch(r'cut (-?\d+)', line):
            card_index = (card_index - int(m[1])) % TOTAL_CARDS
        elif m := re.fullmatch(r'deal with increment (\d+)', line):
            card_index = (card_index * int(m[1])) % TOTAL_CARDS
        else:
            raise ValueError(f'Invalid line: {line!r}')
print(card_index)
