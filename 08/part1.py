import re

def parse(data):
    child = list()
    meta = list()
    children = next(data)
    metadata = next(data)
    for _ in range(children):
        child.append(parse(data))
    for _ in range(metadata):
        meta.append(next(data))
    return(tuple(child), tuple(meta))

def get_meta(data):
    child, meta = data
    return sum(meta) + sum(get_meta(c) for c in child)

def get_values(data):
    children, meta = data
    if len(children) == 0:
        return sum(meta)
    else:
        value = 0
        for index in meta:
            if index > 0 and index <= len(children):
                value += get_values(children[index-1])
        return value

if __name__ == "__main__":
    with open('08/input') as f:
        raw_data = (int(x.group(0)) for x in re.finditer(r'\d+', f.readline()))
    parsed = parse(raw_data)
    print(get_meta(parsed))

    #Part 2
    print(get_values(parsed))