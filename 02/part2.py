from collections import defaultdict
from itertools import combinations

if __name__ == "__main__":
    with open('02/input') as f:
        boxes = [line.strip() for line in f]
    for a, b in combinations(boxes, 2):
        diff = sum(1 for c1, c2 in zip(a, b) if c1 != c2)
        if diff == 1:
            break
    print(''.join(c1 for c1, c2 in zip(a, b) if c1 == c2))