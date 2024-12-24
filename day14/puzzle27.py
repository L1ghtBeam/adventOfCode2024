from functools import reduce
from typing import NamedTuple
from re import match

INPUT_FILE = 'input.txt'
WIDTH, HEIGHT = 101, 103
ELAPSED_TIME = 100

REGEX = r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)"
VALIDATION = ['input_short.txt', 11, 7], 12

class Vector(NamedTuple):
    x: int
    y: int

def main(path: str, width: int, height: int) -> int:
    positions: list[Vector] = []
    velocities: list[Vector] = []

    with open(path) as f:
        for line in f:
            m = match(REGEX, line)
            positions.append(Vector(int(m.group(1)), int(m.group(2))))
            velocities.append(Vector(int(m.group(3)), int(m.group(4))))

    # Quadrant order goes: TL, TR, BL, BR
    quadrants = [0] * 4
    for position, velocity in zip(positions, velocities):
        x = (position.x + velocity.x * ELAPSED_TIME) % width
        y = (position.y + velocity.y * ELAPSED_TIME) % height

        half_x = width // 2
        half_y = height // 2

        quad_index = None
        if x < half_x:
            if y < half_y:
                quad_index = 0
            elif y > half_y:
                quad_index = 2
        elif x > half_x:
            if y < half_y:
                quad_index = 1
            elif y > half_y:
                quad_index = 3
        if quad_index is not None:
            quadrants[quad_index] += 1

    return reduce(lambda u, v: u * v, quadrants)

# test
x = main(*VALIDATION[0])
assert x==VALIDATION[1], f"Test case failed! main({VALIDATION[0]}) returned {x}"

if __name__ == '__main__':
    print(main(INPUT_FILE, WIDTH, HEIGHT))