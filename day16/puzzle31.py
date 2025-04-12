import heapq
import math
from collections import defaultdict
from enum import IntEnum
from typing import NamedTuple


FORWARD_COST = 1
ROTATE_COST = 1000

class Direction(IntEnum):
    NORTH = 0
    WEST = 1
    SOUTH = 2
    EAST = 3

    def coordinate(self):
        if self == Direction.NORTH:
            return -1, 0
        elif self == Direction.WEST:
            return 0, -1
        elif self == Direction.SOUTH:
            return 1, 0
        elif self == Direction.EAST:
            return 0, 1

    def adjacent(self):
        yield Direction((self.value + 1) % 4)
        yield Direction((self.value - 1) % 4)

class Node(NamedTuple):
    row: int
    col: int
    direction: Direction

def main(path: str) -> int:
    maze = []
    with open(path) as f:
        for line in f:
            maze.append(line.rstrip())

    start_node = None
    end_r, end_c = -1, -1
    for r in range(len(maze)):
        for c in range(len(maze[r])):
            if maze[r][c] == 'S':
                start_node = Node(r, c, Direction.EAST)
            elif maze[r][c] == 'E':
                end_r, end_c = r, c

    if start_node is None or end_r == -1 or end_c == -1:
        raise RuntimeError("Couldn't find start or end node")

    # Dijkstra's algorithm
    dist: dict[Node, int | float] = defaultdict(lambda: math.inf)
    dist[start_node] = 0
    heap = [(0, start_node)]
    visited = set()
    while heap:
        distance, node = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(node)

        if node.row == end_r and node.col == end_c:
            return distance

        # check if we can move forward
        dr, dc = node.direction.coordinate()
        r, c = node.row + dr, node.col + dc
        if maze[r][c] != '#':
            # moving forward is a valid move
            adj = Node(r, c, node.direction)
            if adj not in visited and distance + FORWARD_COST < dist[adj]:
                dist[adj] = distance + FORWARD_COST
                heapq.heappush(heap, (distance + FORWARD_COST, adj))

        # check if we can rotate
        for adj_direction in node.direction.adjacent():
            adj = Node(node.row, node.col, adj_direction)
            if adj not in visited and distance + ROTATE_COST < dist[adj]:
                dist[adj] = distance + ROTATE_COST
                heapq.heappush(heap, (distance + ROTATE_COST, adj))

    raise RuntimeError("Couldn't find solution")



if __name__ == '__main__':
    print(main('example_1.txt'),
          main('example_2.txt'),
          main('input.txt'), sep='\n')