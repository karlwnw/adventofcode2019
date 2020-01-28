import re
import math

from collections import defaultdict


def parse(content):
    return list(map(parse_line, content.strip().split("\n")))


def parse_line(row):
    matches = re.findall(r"\s?(\d+) ([A-Z]+),? ", row.strip())
    inputs = [(int(item[0]), item[1]) for item in matches]
    output = re.match(r".+ => (\d+) ([A-Z]+)$", row.strip()).groups()
    return inputs, (int(output[0]), output[1])


def requirements_mapping(reactions):
    # Verify that there is only one rule per Chemical
    assert len(reactions) == len(set(row[-1][1] for row in reactions))

    return {row[-1][1]: (row[-1][0], row[0]) for row in reactions}


def min_usage(reactions, C="FUEL", I="ORE", how_many=1, usage=None, leftovers=None):
    if usage is None:
        usage = defaultdict(int)
    if leftovers is None:
        leftovers = defaultdict(int)

    usage[C] += how_many

    # if C == I:
    if C not in reactions:  # Generalize for any (C, I) pair
        return usage, leftovers

    extra = min(how_many, leftovers[C])
    how_many -= extra
    leftovers[C] -= extra

    quantity, inputs = reactions[C]
    coef = math.ceil(how_many / quantity)

    for qty, name in inputs:
        usage, leftovers = min_usage(reactions, name, I, coef * qty, usage, leftovers)

    leftovers[C] += coef * quantity - how_many

    return usage, defaultdict(int, {k: v for k, v in leftovers.items() if v})


def binary_search(func, low, high, expected):
    while low < high:
        mid = (low + high) // 2
        result = func(mid)
        if result < expected:
            low = mid
        else:
            high = mid - 1
    return low


def get_max_fuel(reactions, max_ore=1e12):
    f = lambda x: min_usage(reactions, how_many=x)[0]["ORE"]
    return binary_search(f, 0, 1000000, max_ore)


if __name__ == "__main__":

    with open("../inputs/day14.input") as f:
        reactions = parse(f.read())

    mapping = requirements_mapping(reactions)

    # Part I
    necessary, waste = min_usage(mapping)
    print(necessary["ORE"])  # 2486514

    # Part II
    value = get_max_fuel(mapping, 1e12)
    print(value)  # 998536

    # Verify that we got the correct value
    necessary, _ = min_usage(mapping, how_many=value)
    assert necessary["ORE"] < 1e12

    necessary, _ = min_usage(mapping, how_many=value + 1)
    assert necessary["ORE"] > 1e12

    # Actually, this could be solved linearly in constant time with 2 data points
    x1, y1 = 1, 2486514
    x2, y2 = 10000000, min_usage(mapping, how_many=10000000)[0]["ORE"]
    # y = ax + b
    slope = (y2 - y1) / (x2 - x1)
    b = y1 - slope * x1
    fuel = round((1e12 - b) / slope)
    assert fuel == value
