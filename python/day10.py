import math

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


if __name__ == "__main__":

    with open("../inputs/day10.input") as f:
        content = f.read()

    # Part I
    print(get_base_point_v2(parse(content)))  # (13, 17) 269

    # Part II
    print(
        nthdestroyed(parse(content), (13, 17), 200)
    )  # (6, 12), ans = 100 * 6 + 12 = 612
