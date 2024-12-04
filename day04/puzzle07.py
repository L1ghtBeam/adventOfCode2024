input_file = 'input.txt'


with open(input_file) as f:
    matrix = f.readlines()

m, n = len(matrix), len(matrix[0]) - 1  # subtract 1 for new line characters

def in_boundary(x: tuple[int, int]) -> bool:
    return 0 <= x[0] < m and 0 <= x[1] < n

all_directions = [(dx, dy) for dx in range(-1, 2) for dy in range(-1, 2) if (dx, dy) != (0, 0)]

word = 'XMAS'

def check_dir(r, c, d) -> bool:
    for i in range(1, len(word)):
        r += d[0]
        c += d[1]
        if not in_boundary((r, c)) or matrix[r][c] != word[i]:
            return False

    return True

count = 0
for r in range(m):
    for c in range(n):
        if matrix[r][c] != word[0]:
            continue

        for d in all_directions:
            if check_dir(r, c, d):
                count += 1

print(count)