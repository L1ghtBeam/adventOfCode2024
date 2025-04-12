import heapq
import math
from collections import defaultdict, deque

from puzzle31 import Direction, Node, FORWARD_COST, ROTATE_COST

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
    frm: dict[Node, list[Node]] = defaultdict(list)

    dist[start_node] = 0
    heap = [(0, start_node)]
    visited = set()
    while heap:
        distance, node = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(node)

        if node.row == end_r and node.col == end_c:
            break

        # check if we can move forward
        dr, dc = node.direction.coordinate()
        r, c = node.row + dr, node.col + dc
        if maze[r][c] != '#':
            # moving forward is a valid move
            adj = Node(r, c, node.direction)
            dist_from_here = distance + FORWARD_COST
            if adj not in visited and dist_from_here <= dist[adj]:
                if dist_from_here < dist[adj]:
                    dist[adj] = dist_from_here
                    heapq.heappush(heap, (dist_from_here, adj))
                    frm[adj].clear()
                frm[adj].append(node)

        # check if we can rotate
        for adj_direction in node.direction.adjacent():
            adj = Node(node.row, node.col, adj_direction)
            dist_from_here = distance + ROTATE_COST
            if adj not in visited and dist_from_here <= dist[adj]:
                if dist_from_here < dist[adj]:
                    dist[adj] = dist_from_here
                    heapq.heappush(heap, (dist_from_here, adj))
                    frm[adj].clear()
                frm[adj].append(node)
    else:
        raise RuntimeError("Couldn't find solution")

    # bfs from end to the start, counting the amount of unique nodes
    q = deque()
    q.append(node)
    visited.clear()
    tiles = set()
    while q:
        node = q.popleft()
        tiles.add((node.row, node.col))
        for adj in frm[node]:
            if adj in visited:
                continue
            q.append(adj)
            visited.add(adj)
    return len(tiles)


if __name__ == '__main__':
    print(main('example_1.txt'),
          main('example_2.txt'),
          main('input.txt'), sep='\n')