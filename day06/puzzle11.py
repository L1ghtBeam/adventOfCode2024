input_file = r'input.txt'

with open(input_file) as f:
    lines = (line.rstrip() for line in f)
    matrix = [[c for c in line] for line in lines]

m, n = len(matrix), len(matrix[0])

def matrix_find(matrix: list[list[str]], x: str):
    for r, row in enumerate(matrix):
        for c, val in enumerate(row):
            if val == x:
                return r, c

r, c = matrix_find(matrix, '^')

def in_boundary(r: int, c: int) -> bool:
    return 0 <= r < m and 0 <= c < n

count = 0
dr, dc = -1, 0
while True:
    # preview next space
    nr, nc = r + dr, c + dc

    # if we're going to move off boundary, then stop looping
    if not in_boundary(nr, nc):
        if matrix[r][c] == '.':
            count += 1
        break

    # if we're looking at a #, rotate right
    if matrix[nr][nc] == '#':
        dr, dc = dc, -dr
        continue

    # fill this cell as 'visited' if it hasn't already
    if matrix[r][c] in ['.', '^']:
        matrix[r][c] = 'X'
        count += 1

    # move next
    r, c = nr, nc


print(count)