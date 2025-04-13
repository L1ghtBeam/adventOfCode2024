from puzzle35 import shortest_path


def main(path, size):
    walls_list = []
    with open(path) as f:
        for i, line in enumerate(f):
            if i == bytes:
                break
            node = tuple(int(val) for val in line.rstrip().split(','))
            walls_list.append(node)

    L, R = 0, len(walls_list)-1
    prev = -1
    walls = set()
    while L <= R:
        m = (L + R) // 2
        if prev < m:
            while prev < m:
                prev += 1
                walls.add(walls_list[prev])
        else:
            while prev > m:
                walls.remove(walls_list[prev])
                prev -= 1
        if (w:=shortest_path(size, walls)) >= 0:
            L = m + 1
        else:
            R = m - 1
    return walls_list[L]

if __name__ == '__main__':
    print(main('example.txt', 6),
          main('input.txt', 70), sep='\n')