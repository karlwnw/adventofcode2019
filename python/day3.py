import re
import sys

from collections import defaultdict

N, S, E, W = 1j, -1j, 1, -1  # Unit vectors
directions = {"U": N, "D": S, "R": E, "L": W}


def parse(text):
    return [
        (direction, int(distance))
        for (direction, distance) in re.findall(r"(U|D|R|L)(\d+)", text)
    ]


def visited(moves):
    visited = set()
    steps = defaultdict(int)
    loc, count = 0, 0
    for (direction, dist) in moves:
        heading = directions[direction]
        for _ in range(dist):
            count += 1
            loc += heading
            visited.add(loc)
            steps[loc] = count
    return visited, steps


def part1(wire1, wire2):
    visited1, _ = visited(wire1)
    visited2, _ = visited(wire2)
    common_points = visited1.intersection(visited2)
    distances = [int(abs(p.imag) + abs(p.real)) for p in common_points]
    return sorted(distances)[0]


def part2(wire1, wire2):
    visited1, steps1 = visited(wire1)
    visited2, steps2 = visited(wire2)
    common_points = visited1.intersection(visited2)
    ordered_points = sorted(
        [(p, steps1[p] + steps2[p]) for p in common_points], key=lambda x: x[1]
    )
    return ordered_points[0][1]


if __name__ == "__main__":
    input_wire1 = parse(sys.stdin.readline())
    input_wire2 = parse(sys.stdin.readline())

    print(part1(input_wire1, input_wire2))

    print(part2(input_wire1, input_wire2))
