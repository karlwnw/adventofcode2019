import math
import unittest

from textwrap import dedent
from itertools import cycle
from fractions import Fraction
from collections import defaultdict, Counter


ASTEROID = "#"
EMPTY = "."


def parse(content):
    lines = content.strip().split("\n")

    points = []
    for y, line in enumerate(lines):
        for x, dot in enumerate(line):
            if dot != EMPTY:
                points.append((x, y))
    return points


def line_eq(A, B):
    Ax, Ay = A
    Bx, By = B
    # y = ax + b
    if By == Ay:
        return 0, By
    if Bx == Ax:
        return Bx

    a = Fraction((By - Ay), (Bx - Ax))
    b = By - (a * Bx)
    return a, b


def get_base_point(points):

    line_to_points = defaultdict(list)
    point_to_points = defaultdict(list)

    for i, p in enumerate(points):
        other_points = points[:i] + points[i + 1 :]
        lines = set()
        for other_p in other_points:
            line = line_eq(p, other_p)
            if line not in lines:
                point_to_points[p].append(other_p)
                lines.add(line)
            if p not in line_to_points[line]:
                line_to_points[line].append(p)

            if other_p not in line_to_points[line]:
                line_to_points[line].append(other_p)

    counter = Counter()
    for key, points in line_to_points.items():
        num = len(points)
        for i, p in enumerate(points):
            # if more than 2 points, each point that are not the first and the last
            # sees 2 other points
            counter[p] += 1 if (num == 2 or i == 0 or i == num - 1) else 2

    base_point, num_visible = counter.most_common()[0]
    # print(base_point, num_visible)

    return base_point, point_to_points[base_point]


def angle(A, B):
    aX, aY = A
    bX, bY = B
    return math.atan2(bX - aX, bY - aY)


def distance(A, B):
    aX, aY = A
    bX, bY = B
    return math.sqrt((bX - aX) ** 2 + (bY - aY) ** 2)


def get_base_point_v2(points):
    point_to_angles = defaultdict(set)

    for p in points:
        for other_p in points:
            if p == other_p:
                continue
            a = angle(p, other_p)
            point_to_angles[p].add(a)

    return len(max(point_to_angles.values(), key=len))


def nthdestroyed(points, base_point, count):
    points.remove(base_point)

    assert count < len(points)

    angle_to_points = defaultdict(list)
    for p in points:
        # a = 2 * math.pi - angle(base_point, p)
        a = math.pi / 2 - angle(base_point, p)
        angle_to_points[a].append(p)

    asteroid_rows = [
        sorted(angle_to_points[a], key=lambda x: distance(base_point, x), reverse=True)
        for a in sorted(angle_to_points.keys())
    ]

    i = 0
    for row in cycle(asteroid_rows):
        if row:
            asteroid = row.pop()
            i += 1
            if i == count:
                return asteroid

    raise RuntimeError("Not Found")


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


if __name__ == "__main__":
    unittest.main(exit=False)

    with open("../inputs/day10.input") as f:
        content = f.read()

    # Part I
    print(get_base_point_v2(parse(content)))  # (13, 17) 269

    # Part II
    print(
        nthdestroyed(parse(content), (13, 17), 200)
    )  # (6, 12), ans = 100 * 6 + 12 = 612
