from functools import reduce
from typing import NamedTuple
from re import match

INPUT_FILE = 'input.txt'
WIDTH, HEIGHT = 101, 103
MAX_SIMULATIONS = 10000

REGEX = r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)"

class Vector(NamedTuple):
    x: int
    y: int

def print_output(positions: list[Vector], width: int, height: int) -> None:
    positions = set(positions)
    for y in range(height):
        for x in range(width):
            if (x, y) in positions:
                print('#',end='')
            else:
                print(' ',end='')
        print()

def main(path: str, width: int, height: int) -> None:
    positions: list[Vector] = []
    velocities: list[Vector] = []

    with open(path) as f:
        for line in f:
            m = match(REGEX, line)
            positions.append(Vector(int(m.group(1)), int(m.group(2))))
            velocities.append(Vector(int(m.group(3)), int(m.group(4))))

    time = 0
    smallest_danger = float('inf')
    while time < MAX_SIMULATIONS:
        quadrants = [0] * 4
        temp: list[Vector] = []
        for position, velocity in zip(positions, velocities):
            x = (position.x + velocity.x) % width
            y = (position.y + velocity.y) % height
            temp.append(Vector(x, y))

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

        danger = reduce(lambda u, v: u * v, quadrants)
        positions = temp
        time += 1

        if danger < smallest_danger:
            smallest_danger = danger
            print(f"Time={time}, danger={danger}")
            print_output(positions, width, height)

if __name__ == '__main__':
    main(INPUT_FILE, WIDTH, HEIGHT)