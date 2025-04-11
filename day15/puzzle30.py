from itertools import takewhile

INPUT_FILE = 'input.txt'

TESTS = [
    [['large_example.txt'], 9021]
]

def main(path: str) -> int:
    matrix: list[list[str]] = []
    moves: list[str] = []
    conversions = {'#': '##', 'O': '[]', '.': '..', '@': '@.'}
    with open(path) as f:
        for line in takewhile(lambda x: x != '\n', f):
            matrix.append([])
            for c in filter(lambda x: x != '\n', line):
                convert = conversions[c]
                for ch in convert:
                    matrix[-1].append(ch)

        moves_iter = (m for line in f for m in filter(lambda x: x!='\n', line))
        for move in moves_iter:
            moves.append(move)

    m, n = len(matrix), len(matrix[0])
    r, c = -1, -1
    found = False
    for r, row in enumerate(matrix):
        for c, val in enumerate(row):
            if val == '@':
                found = True
                break
        if found:
            break
    assert found

    def try_move(r: int, c: int, dr: int, dc: int) -> bool:
        if matrix[r][c] == '@':
            return try_move(r+dr, c+dc, dr, dc)
        if matrix[r][c] == '.':
            return True
        if matrix[r][c] == '#':
            return False

        # cell must be a box
        # move (r, c) to use the left of the box only
        if matrix[r][c] == ']':
            c -= 1

        # horizontal moves are only one tile
        if dc == -1:
            return try_move(r+dr, c+dc, dr, dc)
        if dc == 1:
            return try_move(r+dr, c+dc*2, dr, dc)

        # must be a vertical move. push on the left side
        if not try_move(r+dr, c+dc, dr, dc):
            return False
        # if we pushed the left side of a box above/below us, then that
        # must cover this entire box
        if matrix[r+dr][c+dc] == '[':
            return True
        # we pushed only one side of what's above/below us, so push on the right side
        return try_move(r+dr, c+dc+1, dr, dc)

    def move(r: int, c: int, dr: int, dc: int) -> None:
        if matrix[r][c] == '#':
            raise RuntimeError("Tried to push a wall tile!")
        if matrix[r][c] == '.':
            return
        if matrix[r][c] == '@':
            move(r+dr, c+dc, dr, dc)
            matrix[r+dr][c+dc] = '@'
            matrix[r][c] = '.'

        # we're pushing a box
        # get the left side
        if matrix[r][c] == ']':
            c -= 1

        # horizontal move
        if dr == 0:
            if dc == -1:
                move(r+dr, c+dc, dr, dc)
            elif dc == 1:
                move(r+dr, c+dc*2, dr, dc)
            matrix[r][c+dc] = '['
            matrix[r][c+dc+1] = ']'
            matrix[r][c+1-dc] = '.'
            return

        # vertical move
        box_above = matrix[r+dr][c+dc] == '['
        move(r+dr, c+dc, dr, dc)
        if not box_above:
            move(r+dr, c+dc+1, dr, dc)

        matrix[r+dr][c+dc] = '['
        matrix[r+dr][c+dc+1] = ']'
        matrix[r][c] = '.'
        matrix[r][c+1] = '.'


    move_map = {'^': (-1, 0), '<': (0, -1), '>': (0, 1), 'v': (1, 0)}
    for m in moves:
        dr, dc = move_map[m]
        if try_move(r, c, dr, dc):
            move(r, c, dr, dc)
            r, c = r + dr, c + dc

    res = 0
    for r, row in enumerate(matrix):
        for c, val in enumerate(row):
            if val == 'O':
                res += r * 100 + c
    return res


for test in TESTS:
    x = main(*test[0])
    assert x == test[1], f"Test failed! main({test[0]}) returned {x}"

if __name__ == '__main__':
    print(main(INPUT_FILE))