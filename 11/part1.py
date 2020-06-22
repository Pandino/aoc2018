from functools import lru_cache

SN = 9445

@lru_cache(maxsize=300*300)
def power(x, y):
    a, b = partial(x)
    power_level = ( (a*y + b) // 100) % 10
    return power_level - 5

@lru_cache
def partial(x):
    return (x + 10)**2, (x + 10) * SN

if __name__ == "__main__":
    best = (0, (0, 0), 0)
    for size in range(3, 301):
        for x in range(1, 301-size):
            for y in range(1, 301-size):
                power_level = sum(power(x+dx, y+dy) for dx in range(size) for dy in range(size))
                if power_level > best[0]:
                    best = (power_level, (x, y), size)
                    print(best)
    print(best)
