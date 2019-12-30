from collections import defaultdict

HALT_CODE = 99


class IntCode(object):
    def __init__(self, program):
        # Trick to handle the infinite memory feature:
        # defaultdict + enumerate
        # Also its more efficient than the Program wrapper
        self.program = defaultdict(int, enumerate(program))
        self.pointer = 0
        self.relative_base_offset = 0

    @property
    def opcode(self):
        return self.program[self.pointer] % 100

    def value_for_mode(self, x, mode):
        if mode == 0:
            return self.program[self.program[self.pointer + x + 1]]
        elif mode == 1:
            return self.program[self.pointer + x + 1]
        elif mode == 2:
            return self.program[
                self.program[self.pointer + x + 1] + self.relative_base_offset
            ]
        raise RuntimeError(f"Unknown mode {mode}")

    def run(self, input_code):
        num_parameters = [0, 3, 3, 1, 1, 2, 2, 3, 3, 1]
        while (opcode := self.opcode) != HALT_CODE:
            modes = [int(x) for x in f"{self.program[self.pointer]:0>5}"[:3]][::-1]
            operands = list(
                self.value_for_mode(x, modes[x]) for x in range(num_parameters[opcode])
            )

            if opcode == 1:
                # "Parameters that an instruction writes to
                # will never be in immediate mode (1)"
                offset = self.relative_base_offset if modes[2] == 2 else 0
                self.program[self.program[self.pointer + 3] + offset] = (
                    operands[0] + operands[1]
                )
            elif opcode == 2:
                offset = self.relative_base_offset if modes[2] == 2 else 0
                self.program[self.program[self.pointer + 3] + offset] = (
                    operands[0] * operands[1]
                )
            elif opcode == 3:
                if input_code is None:
                    break

                offset = self.relative_base_offset if modes[0] == 2 else 0
                self.program[self.program[self.pointer + 1] + offset] = input_code
                input_code = None
            elif opcode == 4:
                output = operands[0]
                self.pointer += num_parameters[opcode] + 1
                # print(f"IntCode.output: {output}")
                return output
            elif opcode == 5:
                # "However, if the instruction modifies the instruction self.pointer,
                # that value is used and the instruction self.pointer is not automatically increased."
                # => -3 to cancel out the self.pointer increment
                self.pointer = operands[1] - 3 if operands[0] != 0 else self.pointer
            elif opcode == 6:
                self.pointer = operands[1] - 3 if operands[0] == 0 else self.pointer
            elif opcode == 7:
                offset = self.relative_base_offset if modes[2] == 2 else 0
                self.program[self.program[self.pointer + 3] + offset] = int(
                    operands[0] < operands[1]
                )
            elif opcode == 8:
                offset = self.relative_base_offset if modes[2] == 2 else 0
                self.program[self.program[self.pointer + 3] + offset] = int(
                    operands[0] == operands[1]
                )
            elif opcode == 9:
                # Day 9
                self.relative_base_offset += operands[0]
            else:
                raise RuntimeError(f"Unknown opcode {opcode}")
            self.pointer += num_parameters[opcode] + 1
