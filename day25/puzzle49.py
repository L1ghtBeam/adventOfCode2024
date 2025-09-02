WIDTH, HEIGHT = 5, 7

def decode(buffer: list[str]):
    if buffer[0] == "#####" and buffer[6] == ".....":
        schematic_type = "lock"
    elif buffer[0] == "....." and buffer[6] == "#####":
        schematic_type = "key"
    else:
        raise ValueError(f"Invalid schematic type: {buffer[0]},{buffer[6]}")

    schematic = [sum(1 for j in range(1, HEIGHT-1) if buffer[j][i] == "#") for i in range(WIDTH)]
    return schematic_type, schematic

def main(path: str):
    buffer = []
    locks, keys = [], []
    def add_schematic(schematic_type: str, schematic: list[int]):
        if schematic_type == "lock":
            locks.append(schematic)
        elif schematic_type == "key":
            keys.append(schematic)

    with open(path) as f:
        for line in f:
            line = line.strip()
            if line != "":
                buffer.append(line)
                continue
            add_schematic(*decode(buffer))
            buffer.clear()
    add_schematic(*decode(buffer))

    print(f"{len(locks)} locks and {len(keys)} keys")
    print(f"Comparisons required: {len(locks)*len(keys)}")

    fit = 0
    max_fit = HEIGHT-2
    for key in keys:
        for lock in locks:
            if any(i + j > max_fit for i, j in zip(lock, key)):
                continue
            fit += 1
    return fit

if __name__ == "__main__":
    print("example.txt", main("example.txt"))
    print("input.txt", main("input.txt"))