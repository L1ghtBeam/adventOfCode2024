import string
from collections import deque, defaultdict
from typing import Callable, Iterator

from puzzle41 import Node, matrix_to_map, keypad, dpad

class Keypad:
    def __init__(self, button_map: dict[str, Node], subsequence_func: Callable[[str], int]) -> None:
        self.button_map = button_map

        self.valid_positions = {val for val in button_map.values()}
        self.path_cache: dict[tuple[Node, Node], int] = {}

        self.encode_subsequence = subsequence_func

    def encode(self, sequence: str) -> int:
        i = 0
        out = 0
        start = self.button_map['A']
        while i < len(sequence):
            goal = sequence[i]
            end = self.button_map[goal]

            out += self.find_path(start, end)

            start = end
            i += 1
        return out

    def find_path(self, start: Node, end: Node) -> int:
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
        best_path_len = min(self.encode_subsequence(path) for path in paths)

        self.path_cache[(start, end)] = best_path_len
        return best_path_len

    @staticmethod
    def adjacent(node: Node) -> Iterator[tuple[Node, str]]:
        yield Node(row=node.row - 1, col=node.col), '^'
        yield Node(row=node.row + 1, col=node.col), 'v'
        yield Node(row=node.row, col=node.col - 1), '<'
        yield Node(row=node.row, col=node.col + 1), '>'

def main(path: str) -> int:
    keypad_map = matrix_to_map(keypad)
    dpad_map = matrix_to_map(dpad)

    prev = len
    for _ in range(25):
        directional_pad = Keypad(dpad_map, prev)
        prev = directional_pad.encode

    door_keypad = Keypad(keypad_map, prev)

    complexity = 0
    with open(path) as f:
        for line in f:
            sequence = line.strip()

            print(f"{sequence}: ",end='')
            code_len = door_keypad.encode(sequence)
            print(code_len)

            numeric = sequence.translate(str.maketrans('', '', string.ascii_letters))
            complexity += code_len * int(numeric)

    return complexity

if __name__ == '__main__':
    print(main('input.txt'))