input_file = 'input.txt'

with open(input_file) as f:
    disk_map = f.readline().rstrip()

index_to_id = {}
next_id = 0
for i in range(0, len(disk_map), 2):
    n = int(disk_map[i])
    if not n:
        continue
    index_to_id[i] = next_id
    next_id += 1

L, R = 0, len(disk_map)-1
if R % 2 == 1:
    R -= 1
R_count = 0
pos = 0
res = 0
while L < R:
    # calculate left file blocks
    left_blocks = int(disk_map[L])
    while left_blocks > 0:
        res += index_to_id[L] * pos
        # print(pos,"*",index_to_id[L],L,R,R_count)
        pos += 1
        left_blocks -= 1
    L += 1
    # calculate right files in the free blocks
    right_blocks = int(disk_map[L])
    while right_blocks > 0:
        # go to next R block
        while R_count >= int(disk_map[R]) and L <= R:
            R -= 2
            R_count = 0
        if L >= R:
            break
        res += index_to_id[R] * pos
        # print(pos, "*", index_to_id[R], L, R)
        pos += 1
        right_blocks -= 1
        R_count += 1
    L += 1

# add remaining file blocks
blocks = int(disk_map[L])
while R_count < blocks:
    res += index_to_id[L] * pos
    pos += 1
    R_count += 1

print(res)