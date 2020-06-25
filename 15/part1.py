from blessed import Terminal
from functools import lru_cache
from heapq import heappop, heappush
from operator import attrgetter, itemgetter
from collections import defaultdict

reading_directions = ((0, -1),(-1, 0),(1, 0),(0, 1))
reverse = itemgetter(1, 0)

class Actor():
    def __init__(self, actor_type, position):
        self.type = actor_type
        self.origin = position
        self.position = position
        self.hp = 200
        self.ap = 3
        self.alive = True
        
    
    def __lt__(self, other):
        if type(self) != type(other):
            raise NotImplementedError()
        return reverse(self.position) < reverse(other.position)

    def __str__(self):
        return f'{self.type.upper()}@{self.position}: ({self.hp})'

    def adjacent(self):
        '''Return the coordinates of the adjacent tiles'''
        x, y = self.position
        return set((x+dx, y+dy) for dx, dy in reading_directions)

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.alive = False

    def attack(self, dungeon):
        #Find adjacent targets to attack:
        targets = [actor for actor in dungeon.get_actors() if actor.position in self.adjacent() and actor.type != self.type]
        if targets:
            #Hit the target with the lowest HP
            target = min(targets, key=attrgetter('hp'))
            target.take_damage(self.ap)
            return True
        return False
    
    def update(self, dungeon):
        if not self.alive:
            return True

        if self.attack(dungeon):
            return True
        
        #
        # Move
        #
        # Create a set with the updated position of all obstacles (walls and actors) 
        obstacles = frozenset(dungeon.dungeon.union(actor.position for actor in dungeon.get_actors()))
        # Find all possible target positions around an enemy that are not an obstacle
        enemies = frozenset(actor for actor in dungeon.get_actors() if actor.type != self.type)
        if enemies:
            targets = frozenset(target for actor in enemies for target in actor.adjacent() if target not in obstacles)
            if targets:
                # Calculate all the shortest paths from the actor to the target positions. sorting them by distance and reading order
                # distances = ((shortest_path(self.position, target, obstacles), target) for target in targets)
                # valid_distances = list(distance for distance in distances if distance[0] is not None)
                # if valid_distances:
                #     target = sorted(valid_distances, key=lambda x: (x[0], reverse(x[1])))[0][1]
                #     # Choose the step with the shortest path
                #     distances = ((shortest_path(move, target, obstacles), move) for move in self.adjacent() if move not in obstacles)
                #     valid_distances = (distance for distance in distances if distance[0] is not None)
                #     move = sorted(valid_distances, key=lambda x: (x[0], reverse(x[1])))[0][1]
                #     self.position = move
                move = breath_first(self.position, targets, obstacles)
                if move:
                    self.position = move

            self.attack(dungeon)
            return True

        # No enemies remaining
        return False
    
class Dungeon():
    def __init__(self, map_array):
        self.dungeon = set()
        self.actors = list()
        self._setup_map(map_array)        

    def _setup_map(self, map_array):
        for y, line in enumerate(map_array):
            for x, c in enumerate(line):
                if c == '#':
                    self.dungeon.add((x, y))
                if c == 'E':
                    self.actors.append(Actor('E', (x, y)))
                if c == 'G':
                    self.actors.append(Actor('G', (x, y)))

        self.x_max = max(x for x, _ in self.dungeon) + 1
        self.y_max = max(y for _, y in self.dungeon) + 1

    def get_actors(self):
        yield from (actor for actor in self.actors if actor.alive)
        
    def render(self, term):
        print(term.home + term.clear)
        for actor in self.get_actors():
            print(term.move_xy(*actor.position) + actor.type)
        for (x, y) in self.dungeon:
            print(term.move_xy(x,y) + '#')
        for y, actor in enumerate(self.get_actors()):
            print(term.move_xy(self.x_max+2, y) + str(actor))

        if self.win():
            print(term.move_xy(0, self.y_max+2) + 'Finish.')
        

    def update(self):
        for actor in sorted(self.actors):
            full_turn = actor.update(self)
            if not full_turn:
                break
        dead_actors = [actor for actor in self.actors if not actor.alive]
        for actor in dead_actors:
            self.actors.remove(actor)
        return full_turn

    def win(self):
        classes = set(actor.type for actor in self.actors)
        return len(classes) == 1

@lru_cache
def breath_first(a, targets, obstacles):
    def next_points(point):
        x, y = point
        yield from ((x+dx, y+dy) for dx, dy in reading_directions if (x+dx, y+dy) not in obstacles)

    frontier = []
    come_from = {}
    cost_to = {}
    current = a
    come_from[current] = None
    cost_to[current] = 0
    for source in next_points(current):
        cost_to[source] = 1
        come_from[source] = (current, reverse(source))
        priority = (1, *reverse(source))
        heappush(frontier, (priority, reverse(source), source))

    while len(frontier) > 0:
        _, start, current = heappop(frontier)

        if current in targets:
            break

        for next_point in next_points(current):
            new_cost = cost_to[current] + 1
            if next_point not in cost_to or new_cost < cost_to[next_point] or (new_cost == cost_to[next_point] and start < come_from[next_point][1]):
                cost_to[next_point] = new_cost
                priority = (new_cost, *reverse(next_point))
                heappush(frontier, (priority, start, next_point))
                come_from[next_point] = (current, start)
    else:
        return None
    
    while True:
        if come_from[current][0] == a:
            return current
        current = come_from[current][0]

def test_suite():
    files = [('15/sample2', 27730),
            ('15/sample3', 36334), 
            ('15/sample4', 39514), 
            ('15/sample5', 27755), 
            ('15/sample6', 28944), 
            ('15/sample7', 18740),
            ('15/input', 191575)]

    for testname, score in files:
        with open(testname) as f:
            dungeon = Dungeon(f.readlines())
            turns = 0
            while not dungeon.win():
                full_turn = dungeon.update()
                if full_turn:
                    turns += 1
            final_score = turns * sum(actor.hp for actor in dungeon.get_actors())
            assert(score == final_score)
            print(f'Test {testname} passed.')


if __name__ == "__main__":
    term = Terminal()
    test_suite()    
    # with open('15/input') as f:
    #     dungeon = Dungeon(f.readlines())
    # with term.cbreak():
    #     dungeon.render(term)
    #     term.inkey(timeout=0.05)
    #     turns = 0
    #     while not dungeon.win():
    #         full_turn = dungeon.update()
    #         if full_turn:
    #             turns += 1
    #         dungeon.render(term)
    #         print(turns)
    #         term.inkey(timeout=None)
                
    #     print(f'turns: {turns}')
    #     score = turns * sum(actor.hp for actor in dungeon.get_actors())
    #     print(f'Final score = {score}')
        
        
    