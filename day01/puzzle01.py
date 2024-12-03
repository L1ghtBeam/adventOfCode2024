from pathlib import Path

input_file = Path('day01_input.txt')

left, right = [], []
for line in open(input_file):
    a, b = line.split('   ')
    left.append(int(a))
    right.append(int(b))

left.sort()
right.sort()

dist = 0
for a, b in zip(left, right):
    dist += abs(a - b)

print(dist)