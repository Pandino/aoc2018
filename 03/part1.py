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
    claims = list()
    with open('03/input') as f:
        parser = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')
        for line in f:
            if match := parser.match(line):
                x, y, w, h = (int(match.group(i)) for i in (2, 3, 4, 5))
                claims.append(((x, y), (x + w-1, y + h-1)))
    overlaps = list()
    area = 0
    
    for a, b in itertools.combinations(claims, 2):
        if overlap := overlap2d(a, b):
            overlaps.append(overlap)
            area += square_rect(*overlap)
    
    area = set()
    #let's brute force it
        
    for (x1, y1), (x2, y2) in overlaps:
        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                area.add((x, y))

    print(len(area))        