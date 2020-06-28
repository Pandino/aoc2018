import re
from collections import deque, defaultdict

def simulate2(well_map, bounds, source):
    ''' new strategy:
        1 from source p0, go down until obstacle at pn + 1y, fill p0-pn with |
            1.1 or if pn out of bounds stop
        2 from pn, go (R)ight and (L)eft until a) obstacle or b) no bottom at pb
        3 if both R and L end in a):
            3.1 Fill from R to L with ~
            3.2 goto point 2 with pn-1
        4 if any R and L end in b):
            4.1 Fill from R to L with |
            4.2 From all pb (L or R), goto point 1

        backtracing: take in consideration only y axis. Parent of pb+1 is pn, no pb
                     implemented as a dictionary (come_from)
    '''
    def iswall(point):
        return point in well_map and well_map[point] in '#~'

    def scan_horizontal(origin, dx):
        ''' Return (True, farthest_x) if a wall is found in that direction, (False, farthest) if
        there is no obstacle under farthest
        '''
        x, y = origin
        while True:
            x = x + dx
            if not iswall((x, y+1)):    # going down
                return (False, x)
            elif iswall((x, y)):
                return (True, x-dx)

    min_x, max_x, min_y, max_y = bounds
    frontier = deque()
    frontier.append(source)
    come_from = dict()
    come_from[source] = None

    while len(frontier) > 0:
        x, y = frontier.popleft()

        well_map[(x, y)] = '|'

        if not iswall((x, y+1)):
            if y+1 > max_y:
                continue
            come_from[(x, y+1)] = (x, y)            
            frontier.append((x, y+1))
        else:
            left_wall, left_x = scan_horizontal((x, y), -1)
            right_wall, right_x = scan_horizontal((x, y), +1)
            if left_wall and right_wall:
                for temp_x in range(left_x, right_x + 1):
                    well_map[(temp_x, y)] = '~'
                frontier.appendleft(come_from[(x, y)])
                continue
            else:
                for temp_x in range(left_x, right_x + 1):
                    well_map[(temp_x, y)] = '|'
                if not left_wall and (left_x, y + 1) not in come_from:
                    frontier.append((left_x, y + 1))
                    come_from[(left_x, y + 1)] = (x, y)
                if not right_wall and (right_x, y + 1) not in come_from:
                    frontier.append((right_x, y + 1))
                    come_from[(right_x, y + 1)] = (x, y)
                continue

def inspect(well_map, point):
    c_x, c_y = point
    for y in range(c_y - 30, c_y + 31):
        for x in range(c_x - 40, c_x + 41):
            if (x, y) == (c_x, c_y):
                print('*', end='')
            elif (x, y) in well_map:
                print(well_map[(x, y)], end='')
            else:
                print(' ', end='')
        print()


if __name__ == "__main__":
    well_map = dict()
    source = (500, 0)
    parser = re.compile(r'x=(\d+), y=([.0-9]+)')
    with open('17/input') as f:
        for line in f:
            left, right = line.strip().split(', ')
            a = int(left[2:])
            if '..' in right:
                start, stop = right[2:].split('..')
                for b in range(int(start), int(stop)+1):
                    if left[0] == 'x':
                        well_map[(a,b)] = '#'
                    else:
                        well_map[(b, a)] = '#'
            else:
                b = int(right[2:])
                if left[0] == 'x':
                    well_map[(a,b)] = '#'
                else:
                    well_map[(b, a)] ='#'
            

    min_x = min(x for x, _ in well_map)
    min_y = min(y for _, y in well_map)
    max_x = max(x for x, _ in well_map)
    max_y = max(y for _, y in well_map)

    bounds = (min_x, max_x, min_y, max_y)

    simulate2(well_map, bounds, source)
    tiles = defaultdict(int)
    for tile in (tile for (x, y), tile in  well_map.items() if y >= min_y):
        tiles[tile] += 1
    print(f"Total water:{tiles['~'] + tiles['|']}")
    print(f'Remaining water: {tiles["~"]}')