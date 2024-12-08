from collections import defaultdict
from itertools import combinations
from typing import Generator

input_file = 'input.txt'

antennas = defaultdict(list)

with open(input_file) as f:
    for r, line in enumerate(f):
        line = line.rstrip()
        for c, val in enumerate(line):
            if val != '.':
                antennas[val].append((r,c))

m, n = r + 1, c + 1
def in_boundary(x: tuple[int, int]) -> bool:
    return 0 <= x[0] < m and 0 <= x[1] < n

def find_antinodes(x1: tuple[int, int], x2: tuple[int, int]) -> Generator[tuple[int, int], None, None]:
    r1, c1 = x1
    r2, c2 = x2

    # (dr, dc) is the vector from r1 to r2
    dr = r2 - r1
    dc = c2 - c1

    yield r1-dr, c1-dc
    yield r2+dr, c2+dc

antinodes = set()
for antenna_list in antennas.values():
    for x1, x2 in combinations(antenna_list, 2):
        for x in filter(in_boundary, find_antinodes(x1, x2)):
            antinodes.add(x)

print(len(antinodes))