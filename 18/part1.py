open_acre = (0, 0, 1)
lumberyard = (0, 1, 0)
tree = (1, 0, 0)

def print_world(world, size, symbols):
    for y in range(size[1]+1):
        for x in range(size[0]+1):
            if (x, y) in world:
                print(symbols[world[(x, y)]], end='')
            else:
                print(' ', end='')
        print()

def surrounding(world, point):
    neighbor_deltas = list((x, y) for x in range(-1,2) for y in range(-1, 2) if (x, y) != (0, 0))
    x, y = point
    neighbors = list(world[(x+dx, y+dy)] for dx, dy in neighbor_deltas if (x+dx, y+dy) in world)
    return tuple(sum(row) for row in zip(*neighbors))

def step(world):
    new_world = dict()
    for (x, y), tile in world.items():
        trees, lumbers, opens = surrounding(world, (x, y))
        if tile == open_acre:
            if trees >= 3:
                new_world[(x, y)] = tree
                continue
        if tile == lumberyard:
            if lumbers == 0 or trees == 0:
                new_world[(x, y)] = open_acre
                continue
        if tile == tree:
            if lumbers >= 3:
                new_world[(x, y)] = lumberyard
                continue
        new_world[(x, y)] = tile
    return new_world
        
from collections import defaultdict
def find_reps(collection):
    deltas = list()
    values = list()
    seen_values = defaultdict(list)
    for i, value in enumerate(collection):
        for delta, origin in deltas[:]:
            if values[i-delta] == value:
                if i - delta == origin:
                    return (origin-delta, delta)
            else:
                deltas.remove((delta, origin))
        if value in seen_values:
            for d in seen_values[value]:
                deltas.append((i-d, i))
        seen_values[value].append(i)
        values.append(value)

if __name__ == "__main__":
    acre_type = {'.': open_acre, '#': lumberyard, '|': tree}
    symbols = {value:key for key, value in acre_type.items()}
    world = dict()
    target = 1000000000
    with open('18/input') as f:
        y_max = x_max = 0
        for y, line in enumerate(f):
            if y>y_max: 
                y_max = y
            for x, cell in enumerate(line.strip()):
                if x>x_max:
                    x_max = x
                world[(x,y)] = acre_type[cell]
        size = (x_max, y_max)

    def loop(world):
        while True:
            world = step(world)
            trees, lumbers, opens = (sum(r) for r in zip(*world.values()))
            yield trees*lumbers

    world_save = world.copy()
    a, b = find_reps(loop(world))
    turns = ((target - a) % b) + a
    for _ in range(turns):
        world_save = step(world_save)
        trees, lumbers, opens = (sum(r) for r in zip(*world_save.values()))
    print(trees*lumbers)
