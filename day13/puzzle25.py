from re import compile

INPUT_FILE = 'input.txt'
REGEX = r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)"
A_COST = 3
B_COST = 1
MAX_PRESSES = 100

with open(INPUT_FILE) as f:
    text = f.read()

pattern = compile(REGEX)
res = 0
for machine in pattern.finditer(text):
    A = int(machine.group(1)), int(machine.group(2))
    B = int(machine.group(3)), int(machine.group(4))
    prize = int(machine.group(5)), int(machine.group(6))

    # amount of A presses
    found = False
    for i in range(MAX_PRESSES+1):
        for j in range(MAX_PRESSES+1):
            location = (
                A[0] * i + B[0] * j,
                A[1] * i + B[1] * j,
            )
            if location == prize:
                res += i * A_COST + j * B_COST
                found = True
                break
        if found:
            break

print(res)