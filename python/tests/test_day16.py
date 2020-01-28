import unittest

from day16 import part1, parse, part2


class TestDay16(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(part1(parse("12345678")), [4, 8, 2, 2, 6, 1, 5, 8])
        self.assertEqual(part1(parse("12345678"), 2), [3, 4, 0, 4, 0, 4, 3, 8])
        self.assertEqual(part1(parse("12345678"), 4), [0, 1, 0, 2, 9, 4, 9, 8])

        self.assertEqual(
            part1(parse("80871224585914546619083218645595"), 100)[:8],
            list(map(int, "24176176")),
        )
        self.assertEqual(
            part1(parse("19617804207202209144916044189917"), 100)[:8],
            list(map(int, "73745418")),
        )
        self.assertEqual(
            part1(parse("69317163492948606335995924319873"), 100)[:8],
            list(map(int, "52432133")),
        )

    def test_part2(self):
        self.assertEqual(
            part2(parse("03036732577212944063491565474664"), 100), "84462026"
        )
        self.assertEqual(
            part2(parse("02935109699940807407585447034323"), 100), "78725270"
        )
        self.assertEqual(
            part2(parse("03081770884921959731165446850517"), 100), "53553731"
        )
