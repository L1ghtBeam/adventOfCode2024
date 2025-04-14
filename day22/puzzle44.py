from collections import deque

from puzzle43 import MODULO

def simulate(x: int, changes: deque[int], prices: dict[tuple[int, ...], int], seen: set[tuple[int,...]]) -> int:
    price_before = x % 10

    # step 1
    a = x * 64
    x ^= a
    x %= MODULO

    # step 2
    b = x // 32
    x ^= b
    x %= MODULO

    # step 3
    c = x * 2048
    x ^= c
    x %= MODULO

    price_after = x % 10

    # max size of 4
    if len(changes) == 4:
        changes.popleft()
    changes.append(price_after - price_before)
    sequence = tuple(changes)
    if len(sequence) == 4 and sequence not in seen:
        if price_after != 0 :
            prices[sequence] = price_after + prices.get(sequence, 0)
        seen.add(sequence)

    return x

def main(path: str) -> int:
    prices: dict[tuple[int, ...], int] = {}
    with open(path) as f:
        for line in f:
            changes: deque[int] = deque()
            seen: set[tuple[int,...]] = set()
            val = int(line.rstrip())
            for _ in range(2000):
                val = simulate(val, changes, prices, seen)

    sequence, price = max(prices.items(), key=lambda x: x[1])
    return price

if __name__ == "__main__":
    print(main('example_2.txt'))
    print(main('input.txt'))