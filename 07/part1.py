from collections import defaultdict
import re


if __name__ == "__main__":
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
            print(f'Head found: {step}')
            
    else:
        print('Head not found')
    
    solution = list()
    available = set(heads)
    while len(available) > 0:
        for step in sorted(available):
            if all(d in solution for d in dependencies[step]):
                solution.append(step)
                available.remove(step)
                available.update(graph[step])
                break
    print(''.join(solution))


            


