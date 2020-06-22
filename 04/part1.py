import re
from collections import defaultdict
from operator import itemgetter

def time_ranges(start, stop):
    yield from range(start[3], stop[3])

if __name__ == "__main__":
    with open('04/input') as f:
        schedule = list()
        parser = re.compile(r'\[1518-(\d\d)-(\d\d) (\d\d):(\d\d)\] (.*)')
        guard_parser = re.compile(r'Guard #(\d+) begins shift')
        for line in f:
            if match := parser.match(line):
                schedule.append(tuple(match.group(i) for i in (1, 2, 3, 4, 5)))
        
        guards = dict()
        asleep = None
        for task in sorted(schedule):
            if match := guard_parser.match(task[4]):
                guard = int(match.group(1))
                if guard not in guards:
                    guards[guard] = defaultdict(int)
                continue

            timestamp = tuple(int(task[i]) for i in (0, 1, 2, 3))
            if task[4].startswith('falls'):
                asleep = timestamp
            elif task[4].startswith('wakes'):
                for minute in time_ranges(asleep, timestamp):
                    guards[guard][minute] += 1
        
        # for guard, frequencies in guards.items():
        #     print(guard)
        #     for minute in sorted(frequencies):
        #         print(f'{minute} = {frequencies[minute]}')
            
        top_guard = max(guards, key=lambda x: sum(guards[x].values()))
        top_mins = max(guards[top_guard].items(), key=itemgetter(1))[0]

        print(top_guard * top_mins)

        #Part 2

        flattened = ((g, m, f)  for g, freq in guards.items() for m, f in freq.items())

        topper = max(flattened, key=itemgetter(2))
        print(topper[0]*topper[1])