def step(board, elfs):
    score = sum(board[elf] for elf in elfs)
    units = score % 10
    decines = score // 10
    if decines > 0:
        yield decines
    yield units
    for elf in range(len(elfs)):
        elfs[elf] = (elfs[elf] + board[elfs[elf]] + 1) % len(board)

def part_a(puzzle_input):
    recipes = int(puzzle_input)
    recipes_after = 10
    board = [3, 7]
    elfs = [0, 1]
    while len(board)< recipes+recipes_after:
        score = sum(board[elf] for elf in elfs)
        units = score % 10
        decines = score // 10
        if decines > 0:
            board.append(decines)
        board.append(units)
        for elf in range(len(elfs)):
            elfs[elf] = (elfs[elf] + board[elfs[elf]] + 1) % len(board)
    return ''.join(str(c) for c in board[recipes:recipes+recipes_after])

def part_b(puzzle_input):
    ...

if __name__ == "__main__":
    puzzle_input = '890691'
    #print(f'Part A solution: {part_a(puzzle_input)}')
    assert(part_b('51589') == 9)
    assert(part_b('01245') == 5)
    assert(part_b('92510') == 18)
    assert(part_b('59414') == 2018)