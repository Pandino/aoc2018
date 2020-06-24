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
        for score in step(board, elfs):
            board.append(score)
    return ''.join(str(c) for c in board[recipes:recipes+recipes_after])

def part_b(puzzle_input):
    pattern = [int(c) for c in puzzle_input]
    matches = list()
    board = [3, 7]
    elfs = [0, 1]
    # possible bug: pattern is not matched against the existing board
    matched = False
    while not matched:
        for score in step(board, elfs):
            board.append(score)
            for i in range(len(matches)):
                match = matches[i]
                if score == pattern[match]:
                    matches[i] += 1
                    if matches[i] == len(pattern):
                        matched = True
                        break
                else:
                    matches[i] = 0
            
            if matched:
                break

            if score == pattern[0]:
                matches.append(1)

            
        matches[:] = [m for m in matches if m > 0]
            

    return len(board) - len(pattern)


if __name__ == "__main__":
    puzzle_input = '890691'
    assert(part_a('9') == '5158916779')
    assert(part_a('5') == '0124515891')
    assert(part_a('18') == '9251071085')
    assert(part_a('2018') == '5941429882')
    print(f'Part A solution: {part_a(puzzle_input)}')
    assert(part_b('51589') == 9)
    assert(part_b('01245') == 5)
    assert(part_b('92510') == 18)
    assert(part_b('59414') == 2018)
    print(f'Part B solution: {part_b(puzzle_input)}')