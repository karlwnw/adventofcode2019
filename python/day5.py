from collections import defaultdict

HALT_CODE = 99


class Program(object):
    """Wrapper for infinite memory (Day 9)"""

    def __init__(self, initial):
        self.initial = initial
        self.extra = {}

    def __getitem__(self, key):
        if key < 0:
            raise RuntimeError(f"Invalid negative key {key}")
        try:
            return self.initial[key]
        except IndexError:
            return self.extra.get(key, 0)

    def __setitem__(self, key, value):
        if key < 0:
            raise RuntimeError(f"Invalid negative key {key}")
        try:
            self.initial[key] = value
        except IndexError:
            self.extra[key] = value


def run(program, input_code, pointer=0, relative_base_offset=0):
    """Intcode computer generator"""
    # program = Program(program)

    # Trick to handle the infinite memory feature:
    # defaultdict + enumerate
    # Also its more efficient than the Program wrapper
    program = defaultdict(int, enumerate(program))
    num_parameters = [0, 3, 3, 1, 1, 2, 2, 3, 3, 1]

    def not_finished():
        opcode = program[pointer]
        return opcode != HALT_CODE

    def value_for_mode(x, mode):
        if mode == 0:
            return program[program[pointer + x + 1]]
        elif mode == 1:
            return program[pointer + x + 1]
        elif mode == 2:
            return program[program[pointer + x + 1] + relative_base_offset]
        raise RuntimeError(f"Unknown mode {mode}")

    while not_finished():
        opcode = program[pointer] % 100
        modes = [int(x) for x in f"{program[pointer]:0>5}"[:3]][::-1]
        operands = [value_for_mode(x, modes[x]) for x in range(num_parameters[opcode])]

        if opcode == 1:
            # "Parameters that an instruction writes to
            # will never be in immediate mode (1)"
            offset = relative_base_offset if modes[2] == 2 else 0
            program[program[pointer + 3] + offset] = operands[0] + operands[1]
        elif opcode == 2:
            offset = relative_base_offset if modes[2] == 2 else 0
            program[program[pointer + 3] + offset] = operands[0] * operands[1]
        elif opcode == 3:
            # Add support for multiple inputs in list format
            # for Day 7
            offset = relative_base_offset if modes[0] == 2 else 0
            program[program[pointer + 1] + offset] = (
                input_code.pop(0) if isinstance(input_code, list) else input_code
            )
        elif opcode == 4:
            output = operands[0]
            # print(f"Output: {output}")
            yield output
        elif opcode == 5:
            # "However, if the instruction modifies the instruction pointer,
            # that value is used and the instruction pointer is not automatically increased."
            # => -3 to cancel out the pointer increment
            pointer = operands[1] - 3 if operands[0] != 0 else pointer
        elif opcode == 6:
            pointer = operands[1] - 3 if operands[0] == 0 else pointer
        elif opcode == 7:
            offset = relative_base_offset if modes[2] == 2 else 0
            program[program[pointer + 3] + offset] = int(operands[0] < operands[1])
        elif opcode == 8:
            offset = relative_base_offset if modes[2] == 2 else 0
            program[program[pointer + 3] + offset] = int(operands[0] == operands[1])
        elif opcode == 9:
            # Day 9
            relative_base_offset += operands[0]
        else:
            raise RuntimeError(f"Unknown opcode {opcode}")
        pointer += num_parameters[opcode] + 1
    # return output, pointer, relative_base_offset
    return


def parse(program):
    return list(map(int, program.split(",")))


if __name__ == "__main__":
    with open("../inputs/day5.input") as f:
        program = f.readline()

    # Part I
    outputs = [output for output in run(parse(program), 1)]
    print(outputs[-1])  # 5044655

    # Part II
    print(next(run(parse(program), 5)))  # 7408802
