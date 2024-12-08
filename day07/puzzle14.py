input_file = 'input.txt'
from math import floor, log10

def dfs(li: list[int], index: int, total: int, goal: int) -> bool:
    if total > goal:
        return False

    if index == len(li):
        return total == goal

    base10_len = floor(log10(li[index])) + 1
    concat_total = total * 10 ** base10_len + li[index]

    return dfs(li, index + 1, total + li[index], goal) or   \
        dfs(li, index + 1, total * li[index], goal) or  \
        dfs(li, index + 1, concat_total, goal)

with open(input_file) as f:
    lines = (line.rstrip() for line in f)
    lines = (line.split(' ') for line in lines)
    lines = ((li[0], [li[i] for i in range(1, len(li))]) for li in lines)
    lines = ((int(a[:-1]), [int(b) for b in li]) for a, li in lines)

    result = 0
    for v, nums in lines:
        if len(nums) == 1:
            if nums[0] == v:
                result += v
            continue

        if dfs(nums, 1, nums[0], v):
            result += v

print(result)