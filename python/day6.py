import unittest

from collections import defaultdict, Counter


def parse(line):
    return line.strip().split(")")


def count_orbits(satellites, orbits, o):
    p = orbits.get(o)

    if p is None:
        return 0

    return 1 + count_orbits(satellites, orbits, p)


# Part I
def checksum(orbits):
    satellites_map = defaultdict(list)
    orbits_map = {}

    for A, B in orbits:
        satellites_map[A].append(B)
        orbits_map[B] = A

    count = 0
    for p, satellites in satellites_map.items():
        count += len(satellites) * (1 + count_orbits(satellites_map, orbits_map, p))
        # for s in satellites:
        #     count += 1 + count_orbits(satellites_map, orbits_map, p)

    return count


# Part II
def make_path(satellites_map, orbits_map, o):
    path = []
    p = orbits_map.get(o)

    if p is None:
        return []

    path.append(p)
    return path + make_path(satellites_map, orbits_map, p)


def part2():
    satellites_map = defaultdict(list)
    orbits_map = {}

    for A, B in lines:
        satellites_map[A].append(B)
        orbits_map[B] = A

    san_path = make_path(satellites_map, orbits_map, "SAN")
    you_path = make_path(satellites_map, orbits_map, "YOU")

    commons = set(san_path).intersection(set(you_path))

    san_dict = Counter({o: san_path.index(o) for o in commons})
    san_closest_common_sat = san_dict.most_common()[-1]

    you_dict = Counter({o: you_path.index(o) for o in commons})
    you_closest_common_sat = you_dict.most_common()[-1]

    print(f"{san_closest_common_sat} / {you_closest_common_sat}")
    print(
        f"{san_closest_common_sat[1]} + {you_closest_common_sat[1]} = "
        f"{san_closest_common_sat[1] + you_closest_common_sat[1]}"
    )


class TestDay6(unittest.TestCase):
    def test_example(self):
        test_data = """
        COM)B
        B)C
        C)D
        D)E
        E)F
        B)G
        G)H
        D)I
        E)J
        J)K
        K)L
        """.split()
        self.assertEqual(checksum(list(map(parse, test_data))), 42)


if __name__ == "__main__":
    unittest.main(exit=False)

    with open("../inputs/day6.input") as f:
        lines = list(map(parse, f.readlines()))

    # Part I
    print(checksum(lines))

    # Part II
    part2()
