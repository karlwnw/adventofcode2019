import unittest

from day8 import checksum, parse, decode


class TestDay8(unittest.TestCase):
    def test_checksum(self):
        self.assertEqual(checksum(parse("123456789012"), width=3, height=2), 1)

    def test_decode(self):
        self.assertEqual(
            decode(parse("0222112222120000"), width=2, height=2), [0, 1, 1, 0]
        )
