from collections import deque
from typing import Generator


def adjacent(node: tuple[int, int]) -> Generator[tuple[int, int], None, None]:
    r, c = node
    yield r-1, c
    yield r+1, c
    yield r, c-1
    yield r, c+1

def is_wall(node: tuple[int, int], map: list[str]) -> bool:
    r, c = node
    return map[r][c] == "#"

def distance_from(node: tuple[int, int], map: list[str]) -> dict[tuple[int,int], int]:
    # bfs from node to all nodes in the map
    dist = {}
    depth = 0
    q = deque([node])
    seen = {node}
    while q:
        for _ in range(len(q)):
            node = q.popleft()
            dist[node] = depth

            for adj in adjacent(node):
                if is_wall(adj, map) or adj in seen:
                    continue
                q.append(adj)
                seen.add(adj)

        depth += 1
    return dist

def is_cheat(start: tuple[int, int], end: tuple[int, int], map: list[str]) -> bool:
    middle = tuple((x1+x2)//2 for x1, x2 in zip(start, end))
    return not is_wall(start, map) and not is_wall(end, map) and is_wall(middle, map)

def cheat_time(start: tuple[int, int], end: tuple[int, int], start_dist: dict[tuple[int, int], int],
                     end_dist: dict[tuple[int, int], int]) -> int:
    return start_dist[start] + end_dist[end] + 2

def cheats_through_here(node: tuple[int, int]) -> Generator[tuple[tuple[int, int], tuple[int, int]], None, None]:
    r, c = node
    yield (r-1, c), (r+1, c)
    yield (r+1, c), (r-1, c)
    yield (r, c-1), (r, c+1)
    yield (r, c+1), (r, c-1)

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
            for start, end in cheats_through_here((r, c)):
                if not is_cheat(start, end, map):
                    continue
                time = cheat_time(start, end, start_dist, end_dist)
                time_saved = regular_time - time
                if time_saved >= limit:
                    count += 1
    return count

if __name__ == "__main__":
    print(main("example.txt", 1))
    print(main("input.txt", 100))