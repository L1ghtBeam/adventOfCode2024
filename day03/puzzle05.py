from re import finditer

input_file = r'input.txt'
pattern = r'mul\((\d+),(\d+)\)'

value = 0
with open(input_file) as file:
    matches = (match for line in file for match in finditer(pattern, line))
    for match in matches:
        print(match.group(0))
        a, b = int(match.group(1)), int(match.group(2))
        value += a * b

print(value)