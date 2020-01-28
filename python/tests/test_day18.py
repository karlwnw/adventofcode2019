import unittest

from textwrap import dedent

from day18 import parse, part1, parse2, part2


class TestDay18(unittest.TestCase):
    def test_part1_example1(self):
        content = dedent(
            """
            #########
            #b.A.@.a#
            #########
            """
        )
        grid, starting_point = parse(content)
        self.assertEqual(part1(grid, starting_point), 8)

    def test_part1_example2(self):
        content = dedent(
            """
            ########################
            #f.D.E.e.C.b.A.@.a.B.c.#
            ######################.#
            #d.....................#
            ########################
            """
        )
        grid, starting_point = parse(content)
        self.assertEqual(part1(grid, starting_point), 86)

    def test_part1_example3(self):
        content = dedent(
            """
            ########################
            #...............b.C.D.f#
            #.######################
            #.....@.a.B.c.d.A.e.F.g#
            ########################
            """
        )
        grid, starting_point = parse(content)
        self.assertEqual(part1(grid, starting_point), 132)

    def test_part1_example4(self):
        content = dedent(
            """
            #################
            #i.G..c...e..H.p#
            ########.########
            #j.A..b...f..D.o#
            ########@########
            #k.E..a...g..B.n#
            ########.########
            #l.F..d...h..C.m#
            #################
            """
        )
        grid, starting_point = parse(content)
        self.assertEqual(part1(grid, starting_point), 136)

    def test_part1_example5(self):
        content = dedent(
            """
            ########################
            #@..............ac.GI.b#
            ###d#e#f################
            ###A#B#C################
            ###g#h#i################
            ########################
            """
        )
        grid, starting_point = parse(content)
        self.assertEqual(part1(grid, starting_point), 81)

    def test_part2_example1(self):
        content = dedent(
            """
            #######
            #a.#Cd#
            ##@#@##
            #######
            ##@#@##
            #cB#Ab#
            #######
            """
        )
        grid, starting_points = parse2(content)
        self.assertEqual(part2(grid, starting_points), 8)

    def test_part2_example2(self):
        content = dedent(
            """
            ###############
            #d.ABC.#.....a#
            ######@#@######
            ###############
            ######@#@######
            #b.....#.....c#
            ###############
            """
        )
        grid, starting_points = parse2(content)
        self.assertEqual(part2(grid, starting_points), 24)

    def test_part2_example3(self):
        content = dedent(
            """
            #############
            #DcBa.#.GhKl#
            #.###@#@#I###
            #e#d#####j#k#
            ###C#@#@###J#
            #fEbA.#.FgHi#
            #############
            """
        )
        grid, starting_points = parse2(content)
        self.assertEqual(part2(grid, starting_points), 32)
