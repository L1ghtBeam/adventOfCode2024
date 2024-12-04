from re import finditer

input_file = r'input.txt'
pattern = r"do(?:n't)?\(\)|mul\((\d+),(\d+)\)"

value = 0
enabled = True
with open(input_file) as file:
    matches = (match for line in file for match in finditer(pattern, line))
    for match in matches:
        print(match.group(0), end='')
        if match.group(0) == 'do()':
            enabled = True
        elif match.group(0) == "don't()":
            enabled = False
        else:
            if enabled:
                a, b = int(match.group(1)), int(match.group(2))
                value += a * b
            else:
                print(" IGNORED", end='')
        print()

print(value)