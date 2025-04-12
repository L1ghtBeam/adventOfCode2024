from enum import Enum, auto
from itertools import takewhile


class Instruction(Enum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7


class OperandType(Enum):
    LITERAL = auto()
    COMBO = auto()
    NONE = auto()


instruction_to_operand: dict[Instruction, OperandType] = {
    Instruction.ADV: OperandType.COMBO,
    Instruction.BXL: OperandType.LITERAL,
    Instruction.BST: OperandType.COMBO,
    Instruction.JNZ: OperandType.LITERAL,
    Instruction.BXC: OperandType.NONE,
    Instruction.OUT: OperandType.COMBO,
    Instruction.BDV: OperandType.COMBO,
    Instruction.CDV: OperandType.COMBO,
}


def decode(opcode: int, operand: int, registers: dict[str, int]) -> tuple[Instruction, int]:
    instruction = Instruction(opcode)
    op_type = instruction_to_operand[instruction]

    if op_type == OperandType.LITERAL:
        value = operand
    elif op_type == OperandType.COMBO:
        if operand <= 3:
            value = operand
        elif operand == 4:
            value = registers['A']
        elif operand == 5:
            value = registers['B']
        elif operand == 6:
            value = registers['C']
        else:
            raise RuntimeError("Invalid combo operand of value ", operand)
    elif op_type == OperandType.NONE:
        value = 0
    else:
        raise RuntimeError()

    return instruction, value


def execute(instruction: Instruction, value: int, registers: dict[str, int]) -> int | None:
    if instruction == Instruction.ADV:
        registers['A'] = divide(registers, value)
    elif instruction == Instruction.BXL:
        registers['B'] ^= value
    elif instruction == Instruction.BST:
        registers['B'] = value % 8
    elif instruction == Instruction.JNZ:
        if registers['A'] != 0:
            registers['PC'] = value
    elif instruction == Instruction.BXC:
        registers['B'] ^= registers['C']
    elif instruction == Instruction.OUT:
        return value % 8
    elif instruction == Instruction.BDV:
        registers['B'] = divide(registers, value)
    elif instruction == Instruction.CDV:
        registers['C'] = divide(registers, value)
    return None


def divide(registers, value):
    numerator = registers['A']
    denominator = 2 ** value
    return int(numerator / denominator)

def main(path: str) -> str:
    registers = {'A': 0, 'B': 0, 'C': 0, 'PC': 0}
    with open(path) as f:
        it = iter(f)
        register_info = takewhile(lambda line: line != '\n', it)
        for line in register_info:
            register = line[9]
            value = int(line[12:])
            registers[register] = value

        program_line = next(it)
    program_line = program_line[9:]

    program = [int(val) for val in program_line.split(',')]

    out = []
    while 0 <= registers['PC'] < len(program) - 1:
        # fetch
        opcode = program[registers['PC']]
        operand = program[registers['PC']+1]
        instruction, value = decode(opcode, operand, registers)
        registers['PC'] += 2
        result = execute(instruction, value, registers)
        if result is not None:
            out.append(str(result))
        if registers['PC'] % 2 == 1:
            raise RuntimeError("Program counter became odd, but should never be")
    return ','.join(out)

if __name__ == '__main__':
    print(main('example.txt'),
          main('input.txt'), sep='\n')