import unittest

from day5 import parse, run


class TestDay9(unittest.TestCase):
    def test_examples(self):
        self.assertEqual(
            len(str(next(run(parse("1102,34915192,34915192,7,4,7,99,0"), None)))), 16
        )
        self.assertEqual(
            next(run(parse("104,1125899906842624,99"), None)), 1125899906842624
        )


if __name__ == "__main__":
    unittest.main(exit=False)

    with open("../inputs/day9.input") as f:
        content = f.readline().strip()

    # Part I
    print(next(run(parse(content), 1)))  # 3235019597

    # Part II
    print(next(run(parse(content), 2)))  # 80274
