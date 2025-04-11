from itertools import takewhile

INPUT_FILE = 'input.txt'

TESTS = [
    [['small_example.txt'], 2028],
    [['large_example.txt'], 10092]
]

def main(path: str) -> int:
    matrix: list[list[str]] = []
    moves: list[str] = []
    with open(path) as f:
        for line in takewhile(lambda x: x != '\n', f):
            matrix.append([])
            for c in filter(lambda x: x != '\n', line):
                matrix[-1].append(c)

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

    move_map = {'^': (-1, 0), '<': (0, -1), '>': (0, 1), 'v': (1, 0)}
    for move in moves:
        dr, dc = move_map[move]
        nr, nc = r + dr, c + dc
        depth = 1
        while matrix[nr][nc] == 'O':
            nr, nc = nr + dr, nc + dc
            depth += 1

        # move failed
        if matrix[nr][nc] == '#':
            continue

        while depth > 1:
            matrix[nr][nc] = 'O'
            nr, nc = nr - dr, nc - dc
            depth -= 1

        matrix[nr][nc] = '@'
        matrix[r][c] = '.'
        r, c = nr, nc

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