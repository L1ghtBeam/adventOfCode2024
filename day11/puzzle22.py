from collections import Counter

BLINK_COUNT = 75
INPUT_FILE = 'input.txt'

with open(INPUT_FILE) as f:
    line = f.readline().rstrip()

nums = line.split()
nums = (int(num) for num in nums)

counter = Counter(nums)

for i in range(BLINK_COUNT):
    for n, count in [(k, count) for k, count in counter.items()]:
        counter[n] -= count
        if n == 0:
            counter[n+1] = count + counter.get(n+1, 0)
            continue

        s = str(n)
        if len(s) % 2 == 0:
            half = len(s) // 2
            s1 = s[:half]
            s2 = s[half:]

            if s1 == s2:
                counter[int(s1)] = count * 2 + counter.get(int(s1), 0)
                continue

            counter[int(s1)] = count + counter.get(int(s1), 0)
            counter[int(s2)] = count + counter.get(int(s2), 0)
            continue

        counter[n*2024] = count + counter.get(n*2024, 0)

print(counter.total())