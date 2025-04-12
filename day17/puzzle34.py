from itertools import count, takewhile

from puzzle33 import Instruction, OperandType, instruction_to_operand
from puzzle33 import main as puzzle33_main


def decode(opcode: int, operand: int) -> tuple[Instruction, str]:
    instruction = Instruction(opcode)
    op_type = instruction_to_operand[instruction]

    if op_type == OperandType.LITERAL:
        value = str(operand)
    elif op_type == OperandType.COMBO:
        if operand <= 3:
            value = str(operand)
        elif operand == 4:
            value = 'A'
        elif operand == 5:
            value = 'B'
        elif operand == 6:
            value = 'C'
        else:
            raise RuntimeError("Invalid combo operand of value ", operand)
    elif op_type == OperandType.NONE:
        value = ''
    else:
        raise RuntimeError()

    return instruction, value

def write_asm(in_file: str, out_file: str) -> None:
    registers = {'A': 0, 'B': 0, 'C': 0}
    with open(in_file, 'r') as f:
        it = iter(f)
        register_info = takewhile(lambda line: line != '\n', it)
        for line in register_info:
            register = line[9]
            value = int(line[12:])
            registers[register] = value

        program_line = next(it)
    program_line = program_line[9:]

    program = [int(val) for val in program_line.split(',')]

    with open(out_file, 'w') as f:
        for register in registers:
            f.write(f"Register {register}: {registers[register]}\n")
        f.write('\n')
        i = 0
        while i < len(program):
            f.write(f"{i//2}.\t\t")
            instruction, value = decode(program[i], program[i+1])
            f.write(f"{instruction.name}\t\t{value}\n")
            i += 2

def main(program: list[int]) -> int:
    # recursively backtrack an answer from back to front
    prog = program[::-1]
    ans = 0
    def rec(i):
        nonlocal ans
        if i == len(prog):
            return True
        # make room in our output
        ans = ans << 3
        # try all possible values 1-7
        mask = ~7
        for B in range(8):
            ans = (ans & mask) | B
            B_temp = B ^ 3
            C = ans >> B_temp
            B_temp = B_temp ^ 5

            # check if this value works
            if (B_temp ^ C) & 7 == prog[i] and ans != 0 and rec(i+1):
                return True
        # nothing worked, revert our changes
        ans = ans >> 3
        return False

    if rec(0):
        return ans
    else:
        return -1


if __name__ == '__main__':
    # write_asm('input.txt', 'program.txt')
    res = main([2,4,1,3,7,5,0,3,1,5,4,1,5,5,3,0])
    if res != -1:
        print(res, format(res, '#b'))
        with open('34_test.txt', 'w') as f:
            f.write(f"""Register A: {str(res)}
Register B: 0
Register C: 0

Program: 2,4,1,3,7,5,0,3,1,5,4,1,5,5,3,0""")
        print("Program output:", puzzle33_main('34_test.txt'))
    else:
        print("No solution found")