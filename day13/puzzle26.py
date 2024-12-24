import math
from decimal import Decimal
from re import compile

INPUT_FILE = 'input.txt'
REGEX = r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)"
A_COST = 3
B_COST = 1
OFFSET = 10000000000000
TOL = 1e-9

with open(INPUT_FILE) as f:
    text = f.read()

pattern = compile(REGEX)
res = 0
for machine in pattern.finditer(text):
    P = [
        [Decimal(machine.group(1)), Decimal(machine.group(3))],
        [Decimal(machine.group(2)), Decimal(machine.group(4))]
    ]
    prize = [Decimal(machine.group(5))+OFFSET, Decimal(machine.group(6))+OFFSET]

    if (det := P[0][0]*P[1][1]-P[0][1]*P[1][0]) == 0:
        raise RuntimeError("Determinate zero!")

    # find inverse
    one_over_det = Decimal('1') / det
    P_inverse = [
        [P[1][1], -P[0][1]],
        [-P[1][0], P[0][0]]
    ]
    for r in range(len(P_inverse)):
        for c in range(len(P_inverse[r])):
            P_inverse[r][c] *= one_over_det

    # find inverse
    A, B = P_inverse[0][0] * prize[0] + P_inverse[0][1] * prize[1], \
           P_inverse[1][0] * prize[0] + P_inverse[1][1] * prize[1]

    round_A, round_B = round(A), round(B)
    if math.isclose(A, round_A, rel_tol=0, abs_tol=TOL) and math.isclose(B, round_B, rel_tol=0, abs_tol=TOL):
        res += round_A * A_COST + round_B * B_COST

print(res)