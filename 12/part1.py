import re
from pprint import pp

def pot_print(state):
    for pot in range(min(state), max(state)+1):
        if pot in state:
            print('#', end='')
        else:
            print('.', end='')
    print()

if __name__ == "__main__":
    parser = re.compile(r'([.#]{5}) => ([.#])')
    state = set()
    rules = dict()
    with open('12/input') as f:
        state_line = f.readline()[15:]
        state = set(i for i, c in enumerate(state_line) if c == '#')
        for line in f:
            if match := parser.match(line):
                pattern = match.group(1)
                pattern_hash = 0
                for c in pattern:
                    pattern_hash *= 2
                    if c == '#':
                        pattern_hash += 1
                if match.group(2) == '#':
                    rules[pattern_hash] = True
                else:
                    rules[pattern_hash] = False

    cycles = 0
    new_state = set()
    old_reduced = 0
    while cycles < 500:
        for pot in range(min(state)-2, max(state)+3):
            pot_hash = 0
            for d in range(-2,3):
                pot_hash *= 2
                if pot + d in state:
                    pot_hash += 1
            if pot_hash in rules and rules[pot_hash]:
                new_state.add(pot)
        state = new_state
        new_state = set()
        cycles += 1
        reduced = sum(state)
        print(cycles, reduced, reduced - old_reduced)
        old_reduced = reduced

    print(sum(state))

    print(11373 + (50000000000 - 158)*81)
                