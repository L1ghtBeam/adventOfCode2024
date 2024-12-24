from functools import cache

input_file = 'input.txt'

matrix = []
with open(input_file) as f:
    for line in f:
        matrix.append(line.rstrip())

n, m = len(matrix), len(matrix[0])

def neighbors(r, c):
    yield r-1, c
    yield r+1, c
    yield r, c-1
    yield r, c+1

def in_boundary(x: tuple[int, int]):
    return 0 <= x[0] < n and 0 <= x[1] < m

@cache
def find_ends(r, c) -> int:
    val = int(matrix[r][c])
    if val == 9:
        return 1

    out = 0
    for nr, nc in filter(in_boundary, neighbors(r, c)):
        nval = int(matrix[nr][nc])
        if nval != val + 1:
            continue
        out += find_ends(nr, nc)
    return out

res = 0
for r, row in enumerate(matrix):
    for c, character in enumerate(row):
        val = int(character)
        if val != 0:
            continue
        res += find_ends(r, c)

print(res)