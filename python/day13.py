from day5 import parse, run


BLOCK_ID = 2


def count_blocks(program):
    block_tiles = set()
    intcode = run(program, None)
    output = -1
    i = 1
    x, y = None, None
    while output is not None:
        try:
            output = next(intcode)

            if i % 3 == 0:
                if output == BLOCK_ID:
                    block_tiles.add((x, y))
            elif (i + 1) % 3 == 0:
                y = output
            else:
                x = output

            # print(output)
            i += 1
        except StopIteration:
            break
    return len(block_tiles)


def play(program):
    """todo"""
    program[0] = 2
    score = 0
    intcode = run(program, None)
    output = -1
    i = 1
    x, y = None, None
    while output is not None:
        try:
            output = next(intcode)
        except StopIteration:
            break
    return score


if __name__ == '__main__':

    with open("../inputs/day13.input") as f:
        program = parse(f.readline())

    # Part I
    print(count_blocks(program))  # 326

    # Part II
    # print(play(program))
