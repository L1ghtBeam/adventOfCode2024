MODULO = 16777216

def simulate(x: int) -> int:
    # step 1
    a = x * 64
    x ^= a
    x %= MODULO

    # step 2
    b = x // 32
    x ^= b
    x %= MODULO

    c = x * 2048
    x ^= c
    x %= MODULO

    return x

def main(path: str) -> int:
    out = 0
    with open(path) as f:
        for line in f:
            initial = int(line.rstrip())
            val = initial
            for _ in range(2000):
                val = simulate(val)
            print(f"{initial}: {val}")
            out += val
    return out

if __name__ == "__main__":
    print(main('example.txt'))
    print(main('input.txt'))