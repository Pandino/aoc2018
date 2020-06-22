from collections import defaultdict

if __name__ == "__main__":
    with open('02/input') as f:
        matches = [0, 0]
        for line in f:
            f = defaultdict(int)
            for char in line.strip():
                f[char] += 1
            values = set(f.values())
            if 2 in values:
                matches[0] = matches[0] +1
            if 3 in values:
                matches[1] = matches[1] + 1
        print(matches[0] * matches[1])