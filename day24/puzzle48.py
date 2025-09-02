from collections import defaultdict
from enum import Enum, auto
from typing import Sequence, overload
from itertools import dropwhile
from random import getrandbits

IO_PREFIXES = ('x', 'y', 'z')

class GateType(Enum):
    AND = auto()
    OR = auto()
    XOR = auto()

class Gate:
    @overload
    def __init__(self, line: str):
        pass

    @overload
    def __init__(self, left, gate_type, right, output):
        pass

    def __init__(self, first, *args):
        self.left = None
        self.gateType = None
        self.right = None
        self.output = None

        if len(args) == 3:
            self.construct(first, *args)
            return
        if len(args) != 0:
            raise TypeError('Invalid number of arguments')

        parts = first.split()
        if len(parts) != 5 or parts[3] != "->":
            raise SyntaxError(f"Invalid gate: {first}")

        self.construct(parts[0], GateType[parts[1]], parts[2], parts[4])

    def construct(self, left, gate_type, right, output):
        self.left = left
        self.gateType = gate_type
        self.right = right
        self.output = output

    def __str__(self):
        return f"{self.left} {self.gateType.name} {self.right} -> {self.output}"

    def __repr__(self):
        return f"Gate(\"{str(self)}\")"

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right and self.gateType == other.gateType and self.output == other.output

    def __hash__(self):
        return hash((self.left, self.gateType, self.right, self.output))

class Device:
    def __init__(self, gates: Sequence[Gate]):
        # topological sort to find an eval order
        adj_list = defaultdict(list)
        in_degree = {}
        process_order = []

        # prepare topological sort
        for gate in gates:
            in_degree[gate] = 0
            if not gate.left.startswith(IO_PREFIXES):
                in_degree[gate] += 1
                adj_list[gate.left].append(gate)
            if not gate.right.startswith(IO_PREFIXES):
                in_degree[gate] += 1
                adj_list[gate.right].append(gate)

            if in_degree[gate] == 0:
                process_order.append(gate)

        # topological sort
        i = 0
        while i < len(process_order):
            gate = process_order[i]
            for adj_gate in adj_list[gate.output]:
                in_degree[adj_gate] -= 1
                if in_degree[adj_gate] == 0:
                    process_order.append(adj_gate)
            i += 1

        if len(process_order) != len(gates):
            raise RuntimeError("Topological sort failed")

        self.process_order = process_order

    def eval(self, x, y):
        z = 0
        internal_wires = {}

        for gate in self.process_order:
            left = self.get_wire(gate.left, internal_wires, x, y)
            right = self.get_wire(gate.right, internal_wires, x, y)
            if gate.gateType == GateType.AND:
                out = left and right
            elif gate.gateType == GateType.OR:
                out = left or right
            elif gate.gateType == GateType.XOR:
                out = left != right
            else:
                raise RuntimeError()
            if gate.output.startswith('z'):
                if not out:
                    continue
                bits = int(gate.output[1:])
                z += 1 << bits
            else:
                internal_wires[gate.output] = out

        return z

    @staticmethod
    def get_wire(wire, internal_wires, x, y):
        if wire.startswith('x'):
            bit = int(wire[1:])
            return bool(x & (1 << bit))
        elif wire.startswith('y'):
            bit = int(wire[1:])
            return bool(y & (1 << bit))
        else:
            return internal_wires[wire]

def swap(gate_list, i, j):
    gate_i = gate_list[i]
    gate_j = gate_list[j]
    new_i = Gate(gate_i.left, gate_i.gateType, gate_i.right, gate_j.output)
    new_j = Gate(gate_j.left, gate_j.gateType, gate_j.right, gate_i.output)
    gate_list[i] = new_i
    gate_list[j] = new_j

def score(device, samples):
    total = 0
    for sample in samples:
        evaluated = device.eval(sample[0], sample[1])
        total += (evaluated ^ sample[2]).bit_count()
    return total

def input_bits(gates):
    max_bit = -1
    for gate in gates:
        if gate.left.startswith(IO_PREFIXES):
            max_bit = max(max_bit, int(gate.left[1:]))
        if gate.right.startswith(IO_PREFIXES):
            max_bit = max(max_bit, int(gate.right[1:]))
    return max_bit+1

def main(path):
    with open(path) as f:
        it = iter(f)
        it = dropwhile(lambda line: line != "\n", it)
        next(it)
        gates = []
        for line in it:
            gates.append(Gate(line.strip()))

    # generate samples
    bit_count = input_bits(gates)
    samples = []
    for _ in range(100):
        x = getrandbits(bit_count)
        y = getrandbits(bit_count)
        z = x + y
        samples.append((x,y,z))

    swaps = set()
    while len(swaps) < 8:
        print(f"Starting round {len(swaps)//2+1}")
        # do one round of swapping
        best_score = float('inf')   # smaller is better
        best_pair = None
        for i in range(len(gates)-1):
            if i in swaps:
                continue
            for j in range(i+1, len(gates)):
                if j in swaps:
                    continue
                swap(gates, i, j)
                try:
                    device = Device(gates)
                except RuntimeError:
                    # cycle, skip (undo swap first)
                    swap(gates, i, j)
                    continue
                current_score = score(device, samples)
                if current_score < best_score:
                    best_score = current_score
                    best_pair = (i, j)
                # undo swap
                swap(gates, i, j)

        # keep best pairs swapped
        print(f"Best score: {best_score}")
        swap(gates, best_pair[0], best_pair[1])
        for k in best_pair:
            swaps.add(k)

    # validate
    device = Device(gates)
    final_score = score(device, samples)
    if final_score != 0:
        return f"failed, final score {final_score}"

    return ",".join(sorted(gates[i].output for i in swaps))

print(main("input.txt"))