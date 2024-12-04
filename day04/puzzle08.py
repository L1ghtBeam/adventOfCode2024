input_file = 'input.txt'

with open(input_file) as f:
    matrix = f.readlines()

m, n = len(matrix), len(matrix[0]) - 1

templates = [(a,c,d,b) for a,b in [('M','S'), ('S', 'M')] for c,d in [('M','S'), ('S','M')]]
template_offsets = [(r,c) for r in (-1,1) for c in (-1,1)]
# For each template, character i in template corresponds to the position i in template_offsets. For example, the first
# character in a template has offset -1, -1, the second -1, 1, etc.

def check_xmas(r, c, t):
    # check if the characters at certain offsets of r and c match the corresponding character in template t
    return all(map(
        lambda a,b:a==b,
        (matrix[r+dr][c+dc] for dr,dc in template_offsets),
        t))

count = 0
for r in range(1, m-1):
    for c in range(1, n-1):
        if matrix[r][c] != 'A':
            continue
        for t in templates:
            if check_xmas(r, c, t):
                count += 1

print(count)