import math
import re
import unittest


def parse(row):
    return tuple(map(int, re.findall(r"(-?\d+)", row)))


def pot_energy(coord):
    return sum(map(abs, coord))


def kin_energy(velocity):
    return sum(map(abs, velocity))


def gravity(x, y):
    if x == y:
        return 0
    elif x < y:
        return 1
    else:
        return -1


def velocity(moon, others):
    xV, yV, zV = 0, 0, 0
    for o in others:
        xV += gravity(moon[0], o[0])
        yV += gravity(moon[1], o[1])
        zV += gravity(moon[2], o[2])

    return xV, yV, zV


def move(moons, velocities):
    return [
        (m[0] + velocities[i][0], m[1] + velocities[i][1], m[2] + velocities[i][2])
        for i, m in enumerate(moons)
    ]


def step(moons, velocities=None):
    velocities = velocities or []
    for i, moon in enumerate(moons):
        others = moons[:i] + moons[i + 1 :]
        vX, vY, vZ = velocity(moon, others)
        velocities[i] = (
            velocities[i][0] + vX,
            velocities[i][1] + vY,
            velocities[i][2] + vZ,
        )

    # print(f'velocities = {velocities}')
    return move(moons, velocities), velocities


def total_energy(moons, velocities):
    total_energy = 0
    for i, moon in enumerate(moons):
        total_energy += pot_energy(moon) * kin_energy(velocities[i])
    return total_energy


def run(moons, iterations):
    velocities = [(0, 0, 0)] * len(moons)
    for x in range(iterations):
        moons, velocities = step(moons, velocities)

    return total_energy(moons, velocities)


def lcm(A, B):
    return A * B // math.gcd(A, B)


def transpose(matrix):
    return zip(*matrix)


def by_axes(moons, velocities):
    axis_positions = list(transpose(moons))
    axis_velocities = list(transpose(velocities))
    return zip(axis_positions, axis_velocities)


def find_repeat_cycle(moons):
    """Compute the number of steps that must occur before all
       of the moons' positions and velocities exactly match a
       previous point in time.
    """
    velocities = [(0, 0, 0)] * len(moons)

    count = 1
    found = 0
    seen = {k: set() for k in range(3)}
    counts = {k: 0 for k in range(3)}

    # initial state
    for axis, values in enumerate(by_axes(moons, velocities)):
        seen[axis].add(values)

    while found < 3:
        moons, velocities = step(moons, velocities)
        positions = by_axes(moons, velocities)

        for axis, values in enumerate(positions):
            # Check repeat independently for each axis
            if values in seen[axis] and not counts[axis]:
                found += 1
                counts[axis] = count
            else:
                seen[axis].add(values)

        count += 1

    # print(counts)
    return lcm(lcm(counts[0], counts[1]), counts[2])


class TestDay12(unittest.TestCase):
    def test_examples(self):
        moons = [(-1, 0, 2), (2, -10, -7), (4, -8, 8), (3, 5, -1)]
        self.assertEqual(run(moons, 10), 179)

        moons = [(-8, -10, 0), (5, 5, 10), (2, -7, 3), (9, -8, -3)]
        self.assertEqual(run(moons, 100), 1940)


if __name__ == "__main__":
    unittest.main(exit=False)

    with open("../inputs/day12.input") as f:
        moons = list(map(parse, f.readlines()))

    # Part I
    print(run(moons, 1000))  # 10198

    # Part II
    print(
        find_repeat_cycle(moons)
    )  # {0: 186028, 1: 161428, 2: 144624} LCM = 271442326847376
