from pprint import pprint
from itertools import combinations
from functools import lru_cache
import re

@lru_cache
def distance(a, b):
    ax, ay = a
    bx, by = b
    return abs(bx-ax) + abs(by-ay)

@lru_cache
def total_distance(points):
    return sum(distance(a, b) for a, b in combinations(points, 2))

@lru_cache
def step(points, speeds, times=1):
    new_points = list()
    for point, speed in zip(points, speeds):
        x = point[0] + speed[0] * times
        y = point[1] + speed[1] * times
        new_points.append((x, y))
    return tuple(new_points)

def deriv(points, speeds):
    f_t0 = total_distance(points)
    f_t1 = total_distance(step(points, speeds))
    return f_t1 - f_t0

def find_minimum(points, speeds, initial_delta=1000):    
    time = 0
    delta = initial_delta
    
    while True:
        
        final_points = step(points, speeds, time)
        if delta <= 1:
            break
        if deriv(final_points, speeds) < 0:
            time += delta
        else:
            delta = delta // 2
            time -= delta


    return (time, final_points)

def print_points(points):
    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)

    pixels = set((x-min_x, y-min_y) for x, y in points)

    screen_y = min(max_y-min_y+1, 80)
    screen_x = min(max_x-min_x+1, 80)

    for y in range(screen_y):
        for x in range(screen_x):
            if (x, y) in pixels:
                print('#', end='')
            else:
                print('.', end='')
        print()


if __name__ == "__main__":
    parser = re.compile(r'position=< *(-?\d+), *(-?\d+)> velocity=< *(-?\d+), *(-?\d+)>')
    with open('10/input') as f:
        points = list()
        speeds = list()
        for line in f:
            if match := parser.match(line):
                x, y, dx, dy = [int(match.group(i)) for i in (1, 2, 3, 4)]
            points.append((x, y))
            speeds.append((dx, dy))
        points = tuple(points)
        speeds = tuple(speeds)

    time = 0    
    while True:
        command = input(':>')
        if command == 'p':
            print(f'Time: {time}')
            print_points(points)
            continue
        if command == 's':
            time += 1
            print(f'Time: {time}')
            points = step(points, speeds)
            continue
        if command == 'b':
            time -= 1
            print(f'Time: {time}')
            points = step(points, speeds, -1)
            continue
        if command == 'f':
            time, points = find_minimum(points, speeds)
            continue
        if command == 'q':
            break