def loop(items):
    while True:
        yield from items

if __name__ == "__main__":
    with open('01/input.txt') as f:
        increments = [int(line.strip()) for line in f]
    frequencies = set()
    current = 0
    for frequency in loop(increments):
        current += frequency
        if current not in frequencies:
            frequencies.add(current)
        else:
            print(f'Found repeated frequency: {current}')
            break
            