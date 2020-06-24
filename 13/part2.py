from pprint import pp

left_matrix = ((0, -1), (1, 0))
right_matrix = ((0, 1), (-1, 0))

def dot(vect, m):
    product = [sum(a * b for a, b in zip(vect, col)) for col in zip(*m)]
    return tuple(product)

def find_carts(rail_map):
    carts = list()
    for y, line in enumerate(rail_map):
        for x, c in enumerate(line):
            if c == '>':
                carts.append({'pos': (x,y), 'dir': (1, 0), 'cross': -1, 'inservice': True})
                continue
            if c == 'v':
                carts.append({'pos': (x,y), 'dir': (0, 1), 'cross': -1, 'inservice': True})
                continue
            if c == '<':
                carts.append({'pos': (x,y), 'dir': (-1, 0), 'cross': -1, 'inservice': True})
                continue
            if c == '^':
                carts.append({'pos': (x,y), 'dir': (0, -1), 'cross': -1, 'inservice': True})
                continue
    return carts
            
def tick(carts, rails):
    positions = {cart['pos']: cart for cart in carts if cart['inservice']}
    for cart in sorted(positions.values(), key=lambda p: (p['pos'][1], p['pos'][0])):        
        # Move and check collision:
        new_position = tuple(sum(coords) for coords in zip(cart['pos'], cart['dir']))
        if new_position in positions:
            cart['inservice'] = False
            other = positions[new_position]
            other['inservice'] = False
            continue
        del positions[cart['pos']]
        cart['pos'] = new_position
        positions[new_position] = cart
        x, y = new_position
        dx, dy = cart['dir']
        tile = rails[y][x]
        #Change direction
        if tile == '\\':
            cart['dir'] = (dy, dx)
            continue
        if tile == '/':
            cart['dir'] = (-dy, -dx)
            continue
        if tile == '+':
            cart['cross'] = (cart['cross'] + 1) % 3
            if cart['cross'] == 0:
                cart['dir'] = dot(cart['dir'], left_matrix)
                continue
            if cart['cross'] == 2:
                cart['dir'] = dot(cart['dir'], right_matrix)
                continue
    return [cart for cart in carts if cart['inservice']]

def print_zoom(carts, rails, cart_id=None, zoom=5):
    
    y_max = len(rails)
    if cart_id is not None:
        x0, y0 = carts[cart_id]['pos']
        y_start = y0 - zoom if y0 > zoom else 0
        y_stop = y0 + zoom + 1
        if y_stop > y_max:
            y_stop = y_max
    else:
        y_start = 0
        y_stop = y_max
        
    cart_positions = {cart['pos']: cart['dir'] for cart in carts}
    for y in range(y_start, y_stop):
        x_max = len(rails[y])
        if cart_id is not None:
            x_start = x0 - zoom if x0 > zoom else 0
            x_stop = x0 + zoom + 1
            if x_stop > x_max:
                x_stop = x_max
        else:
            x_start = 0
            x_stop = x_max
        for x in range(x_start, x_stop):
            if (x, y) in cart_positions:
                direction = cart_positions[(x, y)]
                if direction == (0, -1):
                    print('^', end='')
                if direction == (1, 0):
                    print('>', end='')
                if direction == (0, 1):
                    print('v', end='')
                if direction == (-1, 0):
                    print('<', end='')
            else:
                print(rails[y][x], end='')
        print()
    print()


if __name__ == "__main__":
    with open('13/input') as f:
        rails = [line.rstrip() for line in f.readlines()]
    carts = find_carts(rails)
    while True:
        inservice_carts = tick(carts, rails)
        if len(inservice_carts) == 1:
            last_cart_pos = inservice_carts[0]['pos']
            print(f'Last cart in service at {last_cart_pos}')
            break