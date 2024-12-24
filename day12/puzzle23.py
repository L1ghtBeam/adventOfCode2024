from collections import deque

INPUT_FILE = 'input.txt'

matrix = []
with open(INPUT_FILE) as f:
    for line in f:
        matrix.append(line.rstrip())

m, n = len(matrix), len(matrix[0])

def in_boundary(r, c):
    return 0 <= r < m and 0 <= c < n

def neighbors(r, c):
    yield r-1, c
    yield r+1, c
    yield r, c-1
    yield r, c+1


visited = set()
def fill(r, c) -> tuple[int, int]:
    q = deque([(r, c)])
    area, perimeter = 0, 0
    while q:
        r, c = q.popleft()
        area += 1
        for nr, nc in neighbors(r, c):
            if not in_boundary(nr, nc) or matrix[nr][nc] != matrix[r][c]:
                perimeter += 1
            elif (nr, nc) not in visited:
                q.append((nr, nc))
                visited.add((nr, nc))
    return area, perimeter


res = 0
for r, row in enumerate(matrix):
    for c, _ in enumerate(row):
        if (r,c) not in visited:
            visited.add((r,c))
            area, perimeter = fill(r,c)
            res += area * perimeter

print(res)