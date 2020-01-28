import unittest

from day6 import checksum, parse


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
