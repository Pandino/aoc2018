if __name__ == "__main__":
    with open('01/input.txt') as f:
        total_drift = sum(int(line.strip()) for line in f)
    print(f'Part 1: Resulting frequency = {total_drift}')