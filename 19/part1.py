from elfcpu.elfcpu import ElfCpu
from math import sqrt

def sum_of_dividers(d):
    a = 0
    for i in range(1, int(sqrt(d)+1)):
        div, mod = divmod(d, i)
        if mod == 0:
            a += i
            if div != i:
                a += div
    return a


if __name__ == "__main__":
    print(f'Part 1: {sum_of_dividers(958)}')
    print(f'Part 2: {sum_of_dividers(10551358)}')