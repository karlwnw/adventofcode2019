from day5 import parse
from intcode import IntCode

SCAFFOLD = "#"
VOID = "."


def draw(mmap):
    for y, row in enumerate(mmap):
        print()
        print(f"{y:0>2}  ", end="")
        for x, val in enumerate(row):
            print(val, end="")
    print()


def calibrate(program):
    intcode = IntCode(program)

    mmap = []
    row = []
    i = 0
    while True:
        output = intcode.run(None)
        if not output:
            break

        i += 1
        if output == 10:
            if row:
                mmap.append(row)
                row = []
        else:
            row.append(chr(output))

    print("size", len(mmap), len(mmap[0]))
    print("iterations", i)
    draw(mmap)
    return intersections(mmap)


def intersections(mmap):
    count = 0
    total = 0
    for y in range(1, len(mmap) - 1):
        for x in range(1, len(mmap[0]) - 1):
            if mmap[y][x] == SCAFFOLD and all(
                mmap[ny][nx] == SCAFFOLD for (nx, ny) in neighbors((x, y))
            ):
                count += 1
                total += x * y
    return count, total


def neighbors(point):
    return (
        (point[0] + 1, point[1]),
        (point[0] - 1, point[1]),
        (point[0], point[1] + 1),
        (point[0], point[1] - 1),
    )


def navigate(program):
    # todo
    # R,8,L,10
    # R,8
    #     R,2
    #     R,10
    #     R,12
    intcode = IntCode(program)
    instruction = None
    while True:
        output = intcode.run(instruction)
        if not output:
            break
        print(chr(output), end="")


if __name__ == "__main__":
    with open("../inputs/day17.input") as f:
        program = parse(f.readline())

    # Part I
    print(calibrate(program))  # 2804

    # Part II
    program[0] = 2
    print(navigate(program))
