import sys

program = list(map(int, sys.stdin.readline().split(",")))


def run(program, noun, verb):
    program[1] = noun
    program[2] = verb
    length = len(program)
    for pos in range(0, length, 4):
        instruction = program[pos]
        if instruction == 99:
            break
        elif instruction == 1:
            result_pos = program[pos + 3]
            num1_pos = program[pos + 1]
            num2_pos = program[pos + 2]
            program[result_pos] = program[num1_pos] + program[num2_pos]
        elif instruction == 2:
            result_pos = program[pos + 3]
            num1_pos = program[pos + 1]
            num2_pos = program[pos + 2]
            program[result_pos] = program[num1_pos] * program[num2_pos]
        else:
            raise RuntimeError("Unknown instruction {}".format(instruction))
    return program


if __name__ == "__main__":
    # Part I
    print(run(program, 12, 2)[0])

    # Part II
