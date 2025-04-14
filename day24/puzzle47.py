from collections import defaultdict, deque
from enum import Enum, auto
from itertools import takewhile
from typing import Self


class GateType(Enum):
    AND = auto()
    OR = auto()
    XOR = auto()
    CONST = auto()

class GateNode:
    def __init__(self):
        self.type: GateType = GateType.CONST
        self.left: str | None = None
        self.right: str | None = None
        self.value: bool | None = None
        self.adjacent: list[str] = []

    def set_gate(self, gate: GateType, left: str, right: str):
        self.type = gate
        self.left = left
        self.right = right

    def get_value(self) -> bool:
        if self.value is None:
            raise RuntimeError("Tried to get a value on an unevaluated gate")
        return self.value

    def set_value(self, value: bool) -> None:
        if self.type != GateType.CONST:
            raise RuntimeError("Tried to set a value on a non-constant gate")
        self.value = value

    def evaluate(self, gates: dict[str, Self]):
        if self.type == GateType.CONST:
            raise RuntimeError("Cannot evaluate a gate of type CONST")
        left, right = gates[self.left].get_value(), gates[self.right].get_value()

        if self.type == GateType.AND:
            self.value = left and right
        elif self.type == GateType.OR:
            self.value = left or right
        elif self.type == GateType.XOR:
            self.value = left != right

    def reduce_degree(self, in_degree: dict[str, int]) -> list[str]:
        out = []
        for adj in self.adjacent:
            in_degree[adj] -= 1
            if in_degree[adj] == 0:
                out.append(adj)
        return out

    def add_adjacent(self, adj: str) -> None:
        self.adjacent.append(adj)


def make_node(left_gate: str, right_gate: str, operation: str, result: str, gates: dict[str, GateNode],
              in_degree: dict[str, int]):
    gate_type= GateType[operation]
    gates[result].set_gate(gate_type, left_gate, right_gate)

    gates[left_gate].add_adjacent(result)
    gates[right_gate].add_adjacent(result)
    in_degree[result] += 2

def main(path: str) -> int:
    constants = []
    gates: dict[str, GateNode] = defaultdict(GateNode)
    in_degree = defaultdict(int)
    with open(path) as f:
        it = iter(f)
        for line in takewhile(lambda line: line != "\n", it):
            gate_name = line[:3]
            state = line[5] == '1'
            constants.append((gate_name, state))

        for line in it:
            parts = line.split()
            make_node(parts[0], parts[2], parts[1], parts[4], gates, in_degree)

    # evaluate constants
    q = deque()
    for gate_name, state in constants:
        gates[gate_name].set_value(state)
        for ready_node in gates[gate_name].reduce_degree(in_degree):
            q.append(ready_node)

    # evaluate the rest of the nodes
    while q:
        node = q.popleft()
        gates[node].evaluate(gates)
        for ready_node in gates[node].reduce_degree(in_degree):
            q.append(ready_node)

    out = 0
    # find nodes starting with z
    for node in gates.keys():
        if not node.startswith('z') or not gates[node].value:
            continue
        sig = int(node[1:])
        out += 1 << sig

    return out

if __name__ == "__main__":
    print(main('example_1.txt'))
    print(main('example_2.txt'))
    print(main('input.txt'))
