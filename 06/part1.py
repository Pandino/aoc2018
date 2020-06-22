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

def search(start_points, border):
    frontier = deque( (str(cid), coords) for cid, coords in enumerate(start_points) )
    distance_to = { coord: (0, str(cid)) for cid, coord in frontier }
    infiniters = set()
    while len(frontier) > 0:
        
        cid, current = frontier.popleft()
        distance = distance_to[current][0] + 1
        for point in next_coords(current):
            if not is_inside(point, border):
                infiniters.add(cid)
                continue            
            if point in distance_to:
                old_distance, pid = distance_to[point]
                if cid != pid and old_distance == distance:
                    distance_to[point] = (distance, '.')
                continue
            distance_to[point] = (distance, cid)
            frontier.append((cid, point))
    return distance_to, infiniters
                
if __name__ == "__main__":
    with open('06/input') as f:
        coords = list(tuple([int(n.strip()) for n in line.split(',')]) for line in f)
    top = min(coords, key=itemgetter(1))[1] - 1
    bottom = max(coords, key=itemgetter(1))[1] + 1
    left = min(coords)[0] - 1
    right = max(coords)[0] + 1
    border = (left, top, right, bottom)

    distances, infiniters = search(coords, border)

    areas = {cid: sum(1 for point, (_, i) in distances.items() if i == str(cid)) for cid in range(len(coords)) if str(cid) not in infiniters}

    print(max(areas.values()))