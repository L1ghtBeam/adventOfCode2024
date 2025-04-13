from collections import deque
from typing import Generator
from puzzle39 import adjacent, is_wall, distance_from



MIN_CHEAT = 2
MAX_CHEAT = 20

def is_cheat(start: tuple[int, int], end: tuple[int, int], map: list[str]) -> bool:
    return not is_wall(start, map) and not is_wall(end, map)

def in_boundary(node: tuple[int, int], map: list[str]) -> bool:
    return 0 <= node[0] < len(map) and 0 <= node[1] < len(map)

def distance(start: tuple[int, int], end: tuple[int, int]) -> int:
    return sum(abs(x1-x2) for x1, x2 in zip(start, end))

def cheat_time(start: tuple[int, int], end: tuple[int, int], start_dist: dict[tuple[int, int], int],
                     end_dist: dict[tuple[int, int], int]) -> int:
    return start_dist[start] + end_dist[end] + distance(start, end)

def cheats_from_here(start: tuple[int, int], map: list[str]) -> Generator[tuple[tuple[int, int], tuple[int, int]], None, None]:
    q = deque([start])
    seen = {start}
    dist = 0
    while q:
        for _ in range(len(q)):
            end = q.popleft()
            if dist >= MIN_CHEAT:
                yield start, end
            for adj in adjacent(end):
                if adj in seen or not in_boundary(adj, map):
                    continue
                q.append(adj)
                seen.add(adj)
        dist += 1
        if dist > MAX_CHEAT:
            return

def main(path, limit):
    map = []
    with open(path) as f:
        for line in f:
            map.append(line.rstrip())

    start_node = None
    end_node = None
    for r in range(len(map)):
        for c in range(len(map[r])):
            if map[r][c] == "S":
                start_node = (r, c)
            elif map[r][c] == "E":
                end_node = (r, c)
    if not start_node or not end_node:
        return RuntimeError("Couldn't find start or end node")

    start_dist = distance_from(start_node, map)
    end_dist = distance_from(end_node, map)

    regular_time = end_dist[start_node]
    count = 0
    for r in range(1, len(map)-1):
        for c in range(1, len(map[r])-1):
            for start, end in cheats_from_here((r, c), map):
                if not is_cheat(start, end, map):
                    continue
                time = cheat_time(start, end, start_dist, end_dist)
                time_saved = regular_time - time
                if time_saved >= limit:
                    count += 1
    return count

if __name__ == "__main__":
    print(main("example.txt", 72))
    print(main("input.txt", 100))