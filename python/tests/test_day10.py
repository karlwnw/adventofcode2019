import unittest

from textwrap import dedent

from day10 import get_base_point, get_base_point_v2, parse, nthdestroyed


class TestDay10(unittest.TestCase):
    def test_map1(self):
        # [(1, 0), (2, 2), (4, 0), (0, 2), (1, 2), (3, 2), (4, 2), (4, 3), (4, 4)]
        map1 = dedent(
            """
        .#..#
        .....
        #####
        ....#
        ...##
        """
        )
        self.assertEqual(get_base_point(parse(map1))[0], (3, 4), 8)
        self.assertEqual(get_base_point_v2(parse(map1)), 8)

    def test_map2(self):
        map2 = dedent(
            """
        ......#.#.
        #..#.#....
        ..#######.
        .#.#.###..
        .#..#.....
        ..#....#.#
        #..#....#.
        .##.#..###
        ##...#..#.
        .#....####
        """
        )
        self.assertEqual(get_base_point(parse(map2))[0], (5, 8), 33)
        self.assertEqual(get_base_point_v2(parse(map2)), 33)

    def test_map3(self):
        map3 = dedent(
            """
        #.#...#.#.
        .###....#.
        .#....#...
        ##.#.#.#.#
        ....#.#.#.
        .##..###.#
        ..#...##..
        ..##....##
        ......#...
        .####.###. 
        """
        )
        self.assertEqual(get_base_point(parse(map3))[0], (1, 2), 35)
        self.assertEqual(get_base_point_v2(parse(map3)), 35)

    def test_map4(self):
        map4 = dedent(
            """
        .#..#..###
        ####.###.#
        ....###.#.
        ..###.##.#
        ##.##.#.#.
        ....###..#
        ..#.#..#.#
        #..#.#.###
        .##...##.#
        .....#.#..   
        """
        )
        self.assertEqual(get_base_point(parse(map4))[0], (6, 3), 41)
        self.assertEqual(get_base_point_v2(parse(map4)), 41)

    def test_map5(self):
        map5 = dedent(
            """
        .#..##.###...#######
        ##.############..##.
        .#.######.########.#
        .###.#######.####.#.
        #####.##.#.##.###.##
        ..#####..#.#########
        ####################
        #.####....###.#.#.##
        ##.#################
        #####.##.###..####..
        ..######..##.#######
        ####.##.####...##..#
        .#####..#.######.###
        ##...#.##########...
        #.##########.#######
        .####.#.###.###.#.##
        ....##.##.###..#####
        .#.#.###########.###
        #.#.#.#####.####.###
        ###.##.####.##.#..##
        """
        )
        self.assertEqual(get_base_point(parse(map5))[0], (11, 13), 210)
        self.assertEqual(get_base_point_v2(parse(map5)), 210)

        # Part II
        self.assertEqual(nthdestroyed(parse(map5), (11, 13), 200), (8, 2))

    def test_part2(self):
        map6 = dedent(
            """
        .#....###24...#..
        ##...##.13#67..9#
        ##...#...5.8####.
        ..#.....X...###..
        ..#.#.....#....##
        """
        )
        self.assertEqual(nthdestroyed(parse(map6), (8, 3), 1), (8, 1))
        self.assertEqual(nthdestroyed(parse(map6), (8, 3), 2), (9, 0))
        self.assertEqual(nthdestroyed(parse(map6), (8, 3), 3), (9, 1))
