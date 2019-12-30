import unittest

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


class TestDay5(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(next(run(parse("99"), 1), None), None)

        self.assertEqual(next(run(parse("3,0,4,0,99"), 1)), 1)
        self.assertEqual(next(run(parse("3,0,4,0,99"), 28)), 28)

        self.assertEqual(
            next(run(parse("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9"), 0)), 0
        )
        self.assertEqual(
            next(run(parse("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9"), 1)), 1
        )
        self.assertEqual(
            next(run(parse("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9"), 7)), 1
        )

        self.assertEqual(next(run(parse("3,3,1105,-1,9,1101,0,0,12,4,12,99,1"), 0)), 0)
        self.assertEqual(next(run(parse("3,3,1105,-1,9,1101,0,0,12,4,12,99,1"), 1)), 1)
        self.assertEqual(next(run(parse("3,3,1105,-1,9,1101,0,0,12,4,12,99,1"), 18)), 1)

        self.assertEqual(
            next(
                run(
                    parse(
                        "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,"
                        "1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,"
                        "999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
                    ),
                    1,
                )
            ),
            999,
        )
        self.assertEqual(
            next(
                run(
                    parse(
                        "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,"
                        "1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,"
                        "999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
                    ),
                    7,
                )
            ),
            999,
        )
        self.assertEqual(
            next(
                run(
                    parse(
                        "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,"
                        "1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,"
                        "999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
                    ),
                    8,
                )
            ),
            1000,
        )
        self.assertEqual(
            next(
                run(
                    parse(
                        "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,"
                        "1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,"
                        "999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
                    ),
                    9,
                )
            ),
            1001,
        )


if __name__ == "__main__":
    unittest.main(exit=False)

    with open("../inputs/day5.input") as f:
        program = f.readline()

    # Part I
    outputs = [output for output in run(parse(program), 1)]
    print(outputs[-1])  # 5044655

    # Part II
    print(next(run(parse(program), 5)))  # 7408802
