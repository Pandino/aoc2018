from collections import defaultdict

def insert_after(current, value, circle):
    current_pre, current_next = circle[current]
    circle[value] = (current, current_next)
    circle[current] = (circle[current][0], value)
    circle[current_next] = (value, circle[current_next][1])

def remove(current, circle):
    current_pre, current_next = circle[current]
    circle[current_pre] = (circle[current_pre][0], current_next)
    circle[current_next] = (current_pre, circle[current_next][1])
    del circle[current]
    return current_next

def rewind(current, amount, circle):
    while amount > 0:
        current = circle[current][0]
        amount -= 1
    return current

def print_from(from_marble, circle):
    current = from_marble
    for n in range(len(circle)):
        print(f'{current:3} ', end = '')
        current = circle[current][1]
    print()

if __name__ == "__main__":
    current = 0
    marble_circle = {0: (0, 0)}
    marble_limit = 71144*100
    players = 424
    score = defaultdict(int)
    for n in range(1, marble_limit):
        if n % 23 == 0:            
            marble_to_remove = rewind(current, 7, marble_circle)
            score[n%players+1] += n + marble_to_remove
            current = remove(marble_to_remove, marble_circle)
        else:
            insert_after(marble_circle[current][1], n, marble_circle)
            current = n

    print(max(score.values()))