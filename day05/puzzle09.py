from itertools import takewhile
from collections import defaultdict

input_file = r'input.txt'

adj_list = defaultdict(list)

with open(input_file) as f:
    lines = iter(f)
    rules = (line[:-1].split('|') for line in takewhile(lambda x: x != '\n', lines))
    rules = ((int(a), int(b)) for a, b in rules)

    pages = (line[:-1].split(',') for line in lines)
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
                break
        else:
            m = len(page) // 2
            middle_sum += page[m]

print(middle_sum)