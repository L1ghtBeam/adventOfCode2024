from puzzle45 import union
from collections import defaultdict


def find_largest_group(candidate: str,
                       adjacency_set: dict[str, set[str]]) -> list[str]:
    adjacency_list = list(adjacency_set[candidate])
    best = []

    for i in range(len(adjacency_list)-1):
        current = [adjacency_list[i]]
        # find as many nodes which have all the nodes in current as their
        # adjacent
        for j in range(i+1, len(adjacency_list)):
            can_join_group = True
            for group_node in current:
                if group_node not in adjacency_set[adjacency_list[j]]:
                    can_join_group = False
                    break
            if not can_join_group:
                continue
            current.append(adjacency_list[j])

        # see if this current is the new best
        if len(current) >= len(best):
            best = [candidate]
            best.extend(current)

    # this candidate can no longer be a part of any other max groups
    for node in adjacency_list:
        adjacency_set[node].remove(candidate)
    return best

def main(path) -> str:
    adjacency_set = defaultdict(set)
    with open(path) as f:
        for line in f:
            a, b = line.strip().split('-')
            union(a, b, adjacency_set)

    degree_order = [key for key in adjacency_set.keys()]
    degree_order.sort(reverse=True, key=lambda x: len(adjacency_set[x]))

    best = []
    for candidate in degree_order:
        # check if it's impossible for this node to be the candidate
        if len(adjacency_set[candidate]) < len(best):
            continue
        result = find_largest_group(candidate, adjacency_set)
        if len(result) > len(best):
            best = result

    best.sort()
    return ','.join(best)

if __name__ == '__main__':
    print(main('example.txt'))
    print(main('input.txt'))