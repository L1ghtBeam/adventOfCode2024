import time

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

def check_loop(r, c, dr, dc) -> bool:
    visited = set()
    while (r, c, dr, dc) not in visited:
        visited.add((r, c, dr, dc))
        nr, nc = r + dr, c + dc

        if not in_boundary(nr, nc):
            return False

        if matrix[nr][nc] == '#':
            dr, dc = dc, -dr
            continue

        r, c = nr, nc

    return True

count = 0
dr, dc = -1, 0
used_positions = set()
while True:
    # preview next space
    nr, nc = r + dr, c + dc

    # if we're going to move off boundary, then stop looping
    if not in_boundary(nr, nc):
        if matrix[r][c] == '.':
            break

    # if we're looking at a #, rotate right
    if matrix[nr][nc] == '#':
        dr, dc = dc, -dr
        continue

    # if we're not rotating, check if we can place a block in front of us to form a loop
    if (nr, nc) not in used_positions:
        used_positions.add((nr, nc))
        matrix[nr][nc] = '#'
        if check_loop(r, c, dr, dc):
            count += 1
        matrix[nr][nc] = '.'

    # move next
    r, c = nr, nc

print(count)