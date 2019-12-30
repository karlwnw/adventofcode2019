import re
import sys
import unittest

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


class TestDay3(unittest.TestCase):
    def test_part1(self):
        wire1 = "R8,U5,L5,D3"
        wire2 = "U7,R6,D4,L4"
        self.assertEqual(part1(parse(wire1), parse(wire2)), 6)

        wire1 = "R75,D30,R83,U83,L12,D49,R71,U7,L72"
        wire2 = "U62,R66,U55,R34,D71,R55,D58,R83"
        self.assertEqual(part1(parse(wire1), parse(wire2)), 159)

        wire1 = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"
        wire2 = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
        self.assertEqual(part1(parse(wire1), parse(wire2)), 135)

    def tests_part2(self):
        wire1 = "R8,U5,L5,D3"
        wire2 = "U7,R6,D4,L4"
        self.assertEqual(part2(parse(wire1), parse(wire2)), 30)

        wire1 = "R75,D30,R83,U83,L12,D49,R71,U7,L72"
        wire2 = "U62,R66,U55,R34,D71,R55,D58,R83"
        self.assertEqual(part2(parse(wire1), parse(wire2)), 610)

        wire1 = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"
        wire2 = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
        self.assertEqual(part2(parse(wire1), parse(wire2)), 410)


if __name__ == "__main__":
    unittest.main(exit=False)

    input_wire1 = parse(sys.stdin.readline())
    input_wire2 = parse(sys.stdin.readline())

    print(part1(input_wire1, input_wire2))

    print(part2(input_wire1, input_wire2))
