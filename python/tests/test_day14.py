import unittest

from textwrap import dedent

from day14 import requirements_mapping, parse, min_usage


class TestDay14(unittest.TestCase):
    def test_example1(self):
        example1 = dedent(
            """
        10 ORE => 10 A
        1 ORE => 1 B
        7 A, 1 B => 1 C
        7 A, 1 C => 1 D
        7 A, 1 D => 1 E
        7 A, 1 E => 1 FUEL
        """
        )
        mapping = requirements_mapping(parse(example1))
        necessary, waste = min_usage(mapping)
        self.assertEqual(necessary["ORE"], 31)
        self.assertEqual(
            necessary, {"FUEL": 1, "ORE": 31, "A": 28, "B": 1, "C": 1, "D": 1, "E": 1}
        )
        self.assertEqual(waste, {"A": 2})

        # Generalize just for fun
        # How many "A" required to make a "E"?
        necessary, waste = min_usage(mapping, "E", "A")
        self.assertEqual(necessary["A"], 21)
        self.assertEqual(
            necessary, {"E": 1, "A": 21, "B": 1, "C": 1, "D": 1, "ORE": 31}
        )
        self.assertEqual(waste, {"A": 9})

    def test_example2(self):
        example2 = dedent(
            """
        9 ORE => 2 A
        8 ORE => 3 B
        7 ORE => 5 C
        3 A, 4 B => 1 AB
        5 B, 7 C => 1 BC
        4 C, 1 A => 1 CA
        2 AB, 3 BC, 4 CA => 1 FUEL    
        """
        )
        mapping = requirements_mapping(parse(example2))
        necessary, waste = min_usage(mapping)
        self.assertEqual(necessary["ORE"], 165)
        self.assertEqual(
            necessary,
            {
                "FUEL": 1,
                "ORE": 165,
                "AB": 2,
                "BC": 3,
                "CA": 4,
                "A": 10,
                "B": 23,
                "C": 37,
            },
        )
        self.assertEqual(waste, {"B": 1, "C": 3})

        # Generalize just for fun
        # How many "C" required to make 2 "CA"?
        necessary, waste = min_usage(mapping, "CA", "C", 2)
        self.assertEqual(necessary["C"], 8)
        self.assertEqual(necessary, {"CA": 2, "C": 8, "A": 2, "ORE": 23})
        self.assertEqual(waste, {"C": 2})

    def test_example3(self):
        example3 = dedent(
            """
        157 ORE => 5 NZVS
        165 ORE => 6 DCFZ
        44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
        12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
        179 ORE => 7 PSHF
        177 ORE => 5 HKGWZ
        7 DCFZ, 7 PSHF => 2 XJWVT
        165 ORE => 2 GPVTF
        3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT    
        """
        )
        mapping = requirements_mapping(parse(example3))
        necessary, waste = min_usage(mapping)
        self.assertEqual(necessary["ORE"], 13312)

    def test_example4(self):
        example4 = parse(
            """
        2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
        17 NVRVD, 3 JNWZP => 8 VPVL
        53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
        22 VJHF, 37 MNCFX => 5 FWMGM
        139 ORE => 4 NVRVD
        144 ORE => 7 JNWZP
        5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
        5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
        145 ORE => 6 MNCFX
        1 NVRVD => 8 CXFTF
        1 VJHF, 6 MNCFX => 4 RFSQX
        176 ORE => 6 VJHF
        """
        )
        mapping = requirements_mapping(example4)
        necessary, waste = min_usage(mapping)
        self.assertEqual(necessary["ORE"], 180697)
