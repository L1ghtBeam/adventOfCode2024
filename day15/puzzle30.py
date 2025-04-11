from collections import deque
from enum import Enum, auto
from itertools import takewhile
from typing import Self

INPUT_FILE = 'input.txt'

TESTS = [
    [['large_example.txt'], 9021]
]

class TileType(Enum):
    WALL = auto()
    BOX = auto()
    PLAYER = auto()
    EMPTY = auto()

class Tile:
    warehouse: dict[tuple[int, int], Self] = {}

    def __init__(self, tile_type: TileType, row: int, column: int):
        if (row, column) in self.warehouse or (row, column + 1) in self.warehouse:
            raise RuntimeError("Tile row/column is already used by another tile!")

        self.tile_type = tile_type
        self.row = row
        self.column = column

        self.warehouse[(row, column)] = self
        self.warehouse[(row, column + 1)] = self    # two-wide

    def touching(self, dr: int, dc: int) -> list[Self]:
        out = []
        if dc != 1:
            r, c = self.row + dr, self.column + dc
        else:
            # if we're going to the right, start on the right side of our box
            r, c = self.row + dr, self.column+1 + dc
        if (r, c) in self.warehouse:
            out.append(self.warehouse[(r, c)])
        if dr == 0:
            return out
        # if moving up or down, check to the right as well
        c += 1
        if (r, c) in self.warehouse and self.warehouse[(r, c)] not in out:
            out.append(self.warehouse[(r, c)])
        return out

    def move(self, dr: int, dc: int) -> None:
        del self.warehouse[(self.row, self.column)]
        del self.warehouse[(self.row, self.column + 1)]

        r, c = self.row + dr, self.column + dc
        if (r, c) in self.warehouse or (r, c+1) in self.warehouse:
            raise RuntimeError("Tile row/column is already used by another tile!")
        self.warehouse[(r, c)] = self
        self.warehouse[(r, c + 1)] = self
        self.row, self.column = r, c

    def score(self):
        if self.tile_type == TileType.WALL:
            return 0
        return 100 * self.row + self.column

    @classmethod
    def print_warehouse(cls, player_r, player_c):
        M, N = -1, -1
        for tile in cls.warehouse.values():
            M = max(M, tile.row)
            N = max(N, tile.column)
        for r in range(M+1):
            for c in range(N+2):
                if r == player_r and c == player_c:
                    print('@', end='')
                elif (r, c) not in cls.warehouse:
                    print('.', end='')
                else:
                    tile = cls.warehouse[(r, c)]
                    if tile.tile_type == TileType.WALL:
                        print('#', end='')
                    elif tile.tile_type == TileType.BOX:
                        if c == tile.column:
                            print('[', end='')
                        else:
                            print(']', end='')
            print()

    @classmethod
    def clear_tiles(cls):
        cls.warehouse.clear()


def main(path: str) -> int:
    moves: list[str] = []

    char_map: dict[str, TileType] = {'#': TileType.WALL, 'O': TileType.BOX, '.': TileType.EMPTY, '@': TileType.PLAYER}
    player_r, player_c = -1, -1

    with open(path) as f:
        for r, line in enumerate(takewhile(lambda x: x != '\n', f)):
            for c, char in enumerate(filter(lambda x: x != '\n', line)):
                tile_type = char_map[char]
                if tile_type in [TileType.WALL, TileType.BOX]:
                    # for 2-wide tiles, only the left tile has the identity, the other one is empty
                    Tile(tile_type, r, 2*c)
                elif tile_type == TileType.PLAYER:
                    player_r = r
                    player_c = 2*c
                else:
                    pass    # empty tiles are not added to the warehouse dict

        moves_iter = (m for line in f for m in filter(lambda x: x!='\n', line))
        for move in moves_iter:
            moves.append(move)

    def make_move(r: int, c: int, dr: int, dc: int) -> tuple[int, int]:
        # nr, nc represents where we're trying to move to
        nr, nc = r + dr, c + dc
        if (nr, nc) not in Tile.warehouse:
            return nr, nc

        # do a bfs to find all boxes that would be pushed by this move. If we ever see a wall, we cannot move
        to_move: list[Tile] = [Tile.warehouse[(nr, nc)]]
        i = 0
        seen = set()
        while i < len(to_move):
            tile = to_move[i]
            if tile.tile_type == TileType.WALL:
                # we cannot move, return original coordinates
                return r, c
            touching = tile.touching(dr, dc)
            for adj_tile in touching:
                if adj_tile in seen:
                    continue
                to_move.append(adj_tile)
                seen.add(adj_tile)
            i += 1

        # move must be valid, make the move on every tile
        for tile in reversed(to_move):
            tile.move(dr, dc)

        return nr, nc

    move_dirs: dict[str, tuple[int, int]] = {'v': (1, 0), '^': (-1, 0), '>': (0, 1), '<': (0, -1)}
    for move in moves:
        dr, dc = move_dirs[move]
        player_r, player_c = make_move(player_r, player_c, dr, dc)

    seen = set()
    score = 0
    for tile in Tile.warehouse.values():
        if tile not in seen:
            score += tile.score()
            seen.add(tile)
    Tile.clear_tiles()
    return score



for test in TESTS:
    x = main(*test[0])
    assert x == test[1], f"Test failed! main({test[0]}) returned {x}"

if __name__ == '__main__':
    print(main(INPUT_FILE))