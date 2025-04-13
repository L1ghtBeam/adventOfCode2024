from collections import defaultdict
from heapq import heappush, heappop
from typing import Generator


# taxicab distance
def distance(v1, v2) -> int:
    return sum(abs(x1 - x2) for x1, x2 in zip(v1, v2))

def adjacent(node: tuple[int, int]) -> Generator[tuple[int, int], None, None]:
    r, c = node
    yield r-1, c
    yield r+1, c
    yield r, c-1
    yield r, c+1

def in_boundary(size):
    return lambda node: all(0 <= x <= size for x in node)

def shortest_path(size: int, walls: set[tuple[int, int]]) -> int:
    # A* algorithm using distance() as the heuristic
    dist: dict[tuple[int,int], int | float] = defaultdict(lambda: float('inf'))
    start, goal = (0, 0), (size, size)
    dist[start] = 0
    heap = [(0, start)]
    visited = set()

    while heap:
        _, node = heappop(heap)
        if node in visited:
            continue

        if node == goal:
            return dist[node]
        visited.add(node)

        for adj in filter(in_boundary(size), adjacent(node)):
            if adj in walls:
                continue

            if dist[node] + 1 < dist[adj]:
                dist[adj] = dist[node] + 1
                heappush(heap, (dist[adj] + distance(adj, goal), adj))

    return -1

def main(path, size, bytes) -> int:
    walls: set[tuple[int, int]] = set()
    with open(path) as f:
        for i, line in enumerate(f):
            if i == bytes:
                break
            node = tuple(int(val) for val in line.rstrip().split(','))
            walls.add(node)
    return shortest_path(size, walls)

if __name__ == '__main__':
    print(main('example.txt', 6, 12),
          main('input.txt', 70, 1024), sep='\n')