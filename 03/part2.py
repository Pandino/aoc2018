import re
import itertools

def overlap1d(a1, a2, b1, b2):
    if b2 >= a1 and b1 <= a2:
        c1 = min(a2, b2)
        c2 = max(a1, b1)
        return (c2, c1)
    return None

def overlap2d(ra, rb):
    '''return the overlap rectangle formed by a and b or None'''
    (xa1, ya1), (xa2, ya2) = ra
    (xb1, yb1), (xb2, yb2) = rb

    x = overlap1d(xa1, xa2, xb1, xb2)
    if x is not None:
        y = overlap1d(ya1, ya2, yb1, yb2)
        if y is not None:
            return list(zip(x, y))
    return None

def square_rect(a, b):
    return (b[0]-a[0]+1)*(b[1]-a[1]+1)

if __name__ == "__main__":
    claims = dict()
    with open('03/input') as f:
        parser = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')
        for line in f:
            if match := parser.match(line):
                n, x, y, w, h = (int(match.group(i)) for i in (1, 2, 3, 4, 5))
                claims[n] = ((x, y), (x + w-1, y + h-1))
    
    overlapped = set()

    for a, b in itertools.combinations(claims, 2):
        if overlap := overlap2d(claims[a], claims[b]):
            overlapped.add(a)
            overlapped.add(b)

    for i in range(1, len(claims) + 1):
        if i not in overlapped:
            print(i)
            break
    