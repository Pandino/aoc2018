from collections import deque
from operator import itemgetter

cross = ((0, 1),(1, 0),(0, -1),(-1, 0))

def next_coords(current):
    (x, y) = current
    yield from ((x+dx, y+dy) for dx, dy in cross)

def is_inside(point, rectangle):
    l, t, r, b = rectangle
    x, y = point
    return x >= l and x <= r and y >= t and y <= b

def total_distance(point, coords):
    px, py = point
    dist = 0
    for cx, cy in coords:
        dist += abs(px - cx)
        dist += abs(py - cy)        
    return dist


def search(start, points, border, limit=10000):
    frontier = deque((start, ))
    cost_to = dict()
    while len(frontier) > 0:
        current = frontier.popleft()
        if current in cost_to:
            continue
        distance = total_distance(current, points)
        cost_to[current] = distance
        if distance < limit:            
            for point in next_coords(current):
                frontier.append(point)
    return sum(1 for d in cost_to.values() if d < limit)
                
if __name__ == "__main__":
    with open('06/input') as f:
        coords = list(tuple([int(n.strip()) for n in line.split(',')]) for line in f)
    top = min(coords, key=itemgetter(1))[1] - 1
    bottom = max(coords, key=itemgetter(1))[1] + 1
    left = min(coords)[0] - 1
    right = max(coords)[0] + 1
    border = (left, top, right, bottom)
    mid_x = 0
    mid_y = 0
    for x, y in coords:
        mid_x += x
        mid_y += y
    mid_x = mid_x // len(coords)
    mid_y = mid_y // len(coords)
    area = search((mid_x, mid_y), coords, border)
    print(area)