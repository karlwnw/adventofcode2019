import unittest

from day12 import run


class TestDay12(unittest.TestCase):
    def test_examples(self):
        moons = [(-1, 0, 2), (2, -10, -7), (4, -8, 8), (3, 5, -1)]
        self.assertEqual(run(moons, 10), 179)

        moons = [(-8, -10, 0), (5, 5, 10), (2, -7, 3), (9, -8, -3)]
        self.assertEqual(run(moons, 100), 1940)
