import string
from collections import deque, defaultdict
from typing import NamedTuple, Iterator, Callable


class Node(NamedTuple):
    row: int
    col: int

class Keypad:
    def __init__(self, button_map: dict[str, Node], subsequence_func: Callable[[str], str]) -> None:
        self.button_map = button_map

        self.valid_positions = {val for val in button_map.values()}
        self.path_cache: dict[tuple[Node, Node], str] = {}

        self.encode_subsequence = subsequence_func

    def encode(self, sequence: str) -> str:
        i = 0
        out = []
        start = self.button_map['A']
        while i < len(sequence):
            goal = sequence[i]
            end = self.button_map[goal]

            out.append(self.find_path(start, end))

            start = end
            i += 1
        return ''.join(out)

    def find_path(self, start: Node, end: Node) -> str:
        if (start, end) in self.path_cache:
            return self.path_cache[(start, end)]

        q = deque([start])
        dist = defaultdict(lambda : float('inf'))
        dist[start] = 0
        frm = defaultdict(list)
        frm[start].append((None, ''))

        # bfs to find all path to the end
        depth = 0
        found = False
        while not found and q:
            depth += 1
            for _ in range(len(q)):
                node = q.popleft()
                if node == end:
                    found = True
                    break
                for adj, direction in self.adjacent(node):
                    if adj not in self.valid_positions or depth > dist[adj]:
                        continue
                    # if depth <= dist[adj], then add this node as a possible way to get there
                    frm[adj].append((node, direction))
                    # if depth < dist[adj], then this is the first time we're seeing this node
                    if depth < dist[adj]:
                        dist[adj] = depth
                        q.append(adj)

        if end not in frm:
            raise RuntimeError(f"Path could not be found from {start} to {end}")

        # recursive backtracking to get all possible shortest paths
        paths = []
        stack = ['A']
        def rec(node: Node) -> None:
            for prev_node, direction in frm[node]:
                if direction == '':
                    paths.append(''.join(stack[::-1]))
                    continue
                stack.append(direction)
                rec(prev_node)
                stack.pop()
        rec(end)

        # determine the best path by encoding the found sequences
        best_path = None
        best_path_len = float('inf')
        for path in paths:
            full_path = self.encode_subsequence(path)
            if len(full_path) < best_path_len:
                best_path_len = len(full_path)
                best_path = full_path

        if best_path is None:
            raise RuntimeError("No path found")

        self.path_cache[(start, end)] = best_path
        return best_path

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

def main(path: str) -> int:
    keypad_map = matrix_to_map(keypad)
    dpad_map = matrix_to_map(dpad)

    human_dpad = lambda seq: seq
    freezing_dpad = Keypad(dpad_map, human_dpad)
    radiation_dpad = Keypad(dpad_map, freezing_dpad.encode)
    door_keypad = Keypad(keypad_map, radiation_dpad.encode)

    complexity = 0
    with open(path) as f:
        for line in f:
            sequence = line.strip()
            print(f"{sequence}: ", end='')

            code = door_keypad.encode(sequence)
            print(code)

            numeric = sequence.translate(str.maketrans('', '', string.ascii_letters))
            complexity += len(code) * int(numeric)

    return complexity

if __name__ == '__main__':
    print("Example:")
    print(main('example.txt'))
    print("\nInput:")
    print(main('input.txt'))
