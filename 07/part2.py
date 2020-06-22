from collections import defaultdict
import re
from heapq import heappop, heappush


if __name__ == "__main__":
    WORKERS = 5
    JOB_TIME = 60
    graph = defaultdict(set)
    dependencies = defaultdict(set)
    parser = re.compile(r'Step ([A-Z]) must be finished before step ([A-Z]) can begin.')
    with open('07/input') as f:
        for line in f:
            if match:=parser.match(line):
                graph[match.group(1)].add(match.group(2))
                dependencies[match.group(2)].add(match.group(1))
                
    # head: the step without contrains
    heads = list()
    for step in graph:
        if step not in dependencies:
            heads.append(step)
    
    solution = list()
    available = set(heads)
    time = 0
    workers = []
    while len(available) > 0 or len(workers) > 0:
        for step in sorted(available):
            if all(d in solution for d in dependencies[step]):
                if len(workers) < WORKERS:
                    available.remove(step)
                    wait_time = time + JOB_TIME + ord(step) - ord('A')
                    heappush(workers, (wait_time, step))

        if len(workers) > 0:
            elapsed, workload = heappop(workers)
            time = elapsed + 1
            solution.append(workload)
            available.update(graph[workload])

    print(''.join(solution), time)


            


