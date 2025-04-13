import string
from collections import deque
from typing import NamedTuple, Iterator


class Node(NamedTuple):
    row: int
    col: int

class Keypad:
    def __init__(self, button_map: dict[str, Node], start: str) -> None:
        self.button_map = button_map
        self.current = start

        self.valid_positions = {val for val in button_map.values()}
        self.path_cache: dict[tuple[Node, Node], str] = {}

    def encode(self, sequence: str) -> str:
        i = 0
        out = []
        while i < len(sequence):
            goal = sequence[i]
            start = self.button_map[self.current]
            end = self.button_map[goal]

            out.append(self.find_path(start, end))

            self.current = goal
            i += 1
        return ''.join(out)

    def find_path(self, start: Node, end: Node) -> str:
        if (start, end) in self.path_cache:
            return self.path_cache[(start, end)]

        q = deque([start])
        frm = {start: (None, '')}

        # bfs to find path to the end
        while q:
            node = q.popleft()
            if node == end:
                break
            for adj, direction in self.adjacent(node):
                if adj in frm or adj not in self.valid_positions:
                    continue
                frm[adj] = (node, direction)
                q.append(adj)
        else:
            raise RuntimeError(f"Path could not be found from {start} to {end}")

        path_buffer = ['A']
        while node:
            prev_node, direction = frm[node]
            path_buffer.append(direction)
            node = prev_node
        path_buffer.reverse()
        path = ''.join(path_buffer)
        self.path_cache[(start, end)] = path
        return path

    @staticmethod
    def adjacent(node: Node) -> Iterator[tuple[Node, str]]:
        yield Node(row=node.row - 1, col=node.col), '^'
        yield Node(row=node.row + 1, col=node.col), 'v'
        yield Node(row=node.row, col=node.col - 1), '<'
        yield Node(row=node.row, col=node.col + 1), '>'

def matrix_to_map(matrix: list[list[str | None]]) -> dict[str, Node]:
    mapping = {}
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            if matrix[row][col] is None:
                continue
            mapping[matrix[row][col]] = Node(row=row, col=col)
    return mapping

def main(path: str) -> int:
    keypad = [
        ['7', '8', '9'],
        ['4', '5', '6'],
        ['1', '2', '3'],
        [None, '0', 'A']
    ]

    dpad = [
        [None, '^', 'A'],
        ['<', 'v', '>']
    ]

    keypad_map = matrix_to_map(keypad)
    dpad_map = matrix_to_map(dpad)

    door_keypad = Keypad(keypad_map, 'A')
    radiation_dpad = Keypad(dpad_map, 'A')
    freezing_dpad = Keypad(dpad_map, 'A')

    complexity = 0
    with open(path) as f:
        for line in f:
            sequence = line.strip()
            print(f"{sequence}: ", end='')

            code = door_keypad.encode(sequence)
            code = radiation_dpad.encode(code)
            code = freezing_dpad.encode(code)

            print(code)
            numeric = sequence.translate(str.maketrans('', '', string.ascii_letters))
            print(int(numeric))
            print(len(code))
            complexity += len(code) * int(numeric)

    return complexity

if __name__ == '__main__':
    print(main('example.txt'))
