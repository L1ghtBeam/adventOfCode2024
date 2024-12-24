from enum import Enum, auto
from collections import deque

INPUT_FILE = 'input.txt'

# direction of a perimeter is defined as the name of the side
# from the region to outside the region. The perimeter on the top
# is 'up'
class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


matrix = []
with open(INPUT_FILE) as f:
    for line in f:
        matrix.append(line.rstrip())

m, n = len(matrix), len(matrix[0])

def in_boundary(r: int, c: int) -> bool:
    return 0 <= r < m and 0 <= c < n

def neighbors(r: int, c: int) -> tuple[int, int, Direction]:
    yield r-1, c, Direction.UP
    yield r+1, c, Direction.DOWN
    yield r, c-1, Direction.LEFT
    yield r, c+1, Direction.RIGHT

visited = set()
def fill(r: int, c: int) -> tuple[int, set[tuple[int, int, Direction]]]:
    q = deque([(r, c)])
    area, perimeter = 0, set()
    while q:
        r, c = q.popleft()
        area += 1
        for nr, nc, direction in neighbors(r, c):
            if not in_boundary(nr, nc) or matrix[nr][nc] != matrix[r][c]:
                perimeter.add((nr, nc, direction))
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

            # compute perimeter
            sides = 0
            while perimeter:
                sides += 1
                nr, nc, direction = perimeter.pop()
                if direction in [Direction.UP, Direction.DOWN]:
                    # remove contiguous matching sides in nearby columns
                    dc = 1
                    while nc + dc < n and (x:=(nr, nc+dc, direction)) in perimeter:
                        perimeter.remove(x)
                        dc += 1
                    dc = -1
                    while nc + dc >= 0 and (x:=(nr, nc+dc, direction)) in perimeter:
                        perimeter.remove(x)
                        dc -= 1
                else:
                    # remove contiguous matching sides in nearby rows
                    dr = 1
                    while nr + dr < m and (x:=(nr+dr, nc, direction)) in perimeter:
                        perimeter.remove(x)
                        dr += 1
                    dr = -1
                    while nr + dr >= 0 and (x := (nr + dr, nc, direction)) in perimeter:
                        perimeter.remove(x)
                        dr -= 1

            res += area * sides

print(res)