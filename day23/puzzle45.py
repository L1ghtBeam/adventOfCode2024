from collections import defaultdict


def union(a: str, b: str, adjacency_set: dict[str, set[str]]) -> None:
    adjacency_set[a].add(b)
    adjacency_set[b].add(a)

def find_trios(candidates: list[str],
               adjacency_set: dict[str, set[str]]) -> list[tuple[str, str, str]]:
    results = []
    for candidate in candidates:
        adjacent = list(adjacency_set[candidate])
        # check if any two adjacent nodes are adjacent with each other
        for i in range(len(adjacent)-1):
            for j in range(i+1, len(adjacent)):
                if adjacent[j] in adjacency_set[adjacent[i]]:
                    results.append((candidate, adjacent[i], adjacent[j]))
        # remove this candidate from the adjacency set, it can no longer be
        # a part of another trio
        for node in adjacent:
            adjacency_set[node].remove(candidate)
    return results

def main(path) -> int:
    adjacency_set = defaultdict(set)
    candidates = []
    seen = set()
    with open(path) as f:
        for line in f:
            a, b = line.strip().split('-')
            union(a, b, adjacency_set)

            if a not in seen:
                seen.add(a)
                if a.startswith('t'):
                    candidates.append(a)
            if b not in seen:
                seen.add(b)
                if b.startswith('t'):
                    candidates.append(b)

    result = find_trios(candidates, adjacency_set)
    for trio in result:
        print(*trio, sep=',')
    return len(result)

if __name__ == '__main__':
    print("Example:")
    print(main('example.txt'))
    print("Input:")
    print(main('input.txt'))