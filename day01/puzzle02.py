from pathlib import Path
from collections import defaultdict

input_file = Path('day01_input.txt')

left = []
count = defaultdict(int)
for line in open(input_file):
    a, b = line.split('   ')
    left.append(int(a))
    count[int(b)] += 1

similarity = 0
for n in left:
    similarity += n * count[n]

print(similarity)