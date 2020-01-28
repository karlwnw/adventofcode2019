import unittest

from day3 import parse, part1, part2


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
