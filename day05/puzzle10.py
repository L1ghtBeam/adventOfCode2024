from itertools import takewhile
from collections import defaultdict

input_file = r'input.txt'

adj_list = defaultdict(list)

def find_middle(record: list[int], graph: dict[int, list[int]]) -> int:
    stack = []
    unvisited = set(record)

    def topo_sort(n: int):
        for adj in adj_list[n]:
            if adj in unvisited:
                unvisited.remove(adj)
                topo_sort(adj)
        stack.append(n)

    while unvisited:
        topo_sort(unvisited.pop())

    # stack is now in reverse order, but since we need the middle this doesn't
    # matter
    m = len(stack) // 2
    return stack[m]


with open(input_file) as f:
    # not all lines end with a newline character, this will deal with that
    # properly
    lines = (line.rstrip() for line in f)

    rules = (line.split('|') for line in takewhile(lambda x: x != '', lines))
    rules = ((int(a), int(b)) for a, b in rules)

    pages = (line.split(',') for line in lines)
    pages = ([int(a) for a in page] for page in pages)

    # a -> b
    for a, b in rules:
        adj_list[a].append(b)

    middle_sum = 0
    for page in pages:
        # seen contains values already 'seen' in the page
        seen = set()
        for n in page:
            seen.add(n)

            # check every value that we know must come after this one. If any of them have been seen before, we know
            # the page is invalid
            if any(map(lambda x: x in seen, adj_list[n])):
                middle_sum += find_middle(page, adj_list)
                break

print(middle_sum)