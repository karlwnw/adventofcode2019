import itertools
import unittest

from day5 import parse
from intcode import IntCode


class Amplifier(IntCode):
    pass


def permutations(L):
    """permutation implementation, just for fun
    should be the same as itertool.permutations
    """
    if not L:
        return [()]
    ans = []
    for i, item in enumerate(L):
        sub_L = L[:i] + L[i + 1 :]
        perms_sub_L = permutations(sub_L)
        for x in perms_sub_L:
            ans.append((item, *x))
    return ans


def amplifiers(program, phase_settings):
    """
        program: The Intcode computer instructions

        phase_settings : a list of 5 integers between [0, 4]
        Each phase setting is used exactly once

            O-------O  O-------O  O-------O  O-------O  O-------O
        0 ->| Amp A |->| Amp B |->| Amp C |->| Amp D |->| Amp E |-> (to thrusters)
            O-------O  O-------O  O-------O  O-------O  O-------O
    """
    # "The first amplifier's input signal value is 0"
    signal = 0

    for phase in phase_settings:
        amp = Amplifier(program)
        amp.run(phase)
        signal = amp.run(signal)

    return signal


def part1(program):
    permutations = itertools.permutations([0, 1, 2, 3, 4])

    max_output = 0
    for permutation in permutations:
        output = amplifiers(program, permutation)
        max_output = max(output, max_output)

    return max_output


def feedback_amplifiers(program, phase_settings):
    """
        program: The Intcode computer instructions

        phase_settings : a list of 5 integers between [5, 9]
        Each phase setting is used exactly once

              O-------O  O-------O  O-------O  O-------O  O-------O
        0 -+->| Amp A |->| Amp B |->| Amp C |->| Amp D |->| Amp E |-.
           |  O-------O  O-------O  O-------O  O-------O  O-------O |
           |                                                        |
           '--------------------------------------------------------+
                                                                    |
                                                                    v
                                                             (to thrusters)
    """
    # "The first amplifier's input signal value is 0"
    signal = 0

    amps = [Amplifier(program) for _ in range(5)]

    # init with phase settings
    for i, phase in enumerate(phase_settings):
        amps[i].run(phase)
        signal = amps[i].run(signal)

    # loop until program finishes
    for i in itertools.cycle(range(5)):
        output = amps[i].run(signal)
        if output is None:
            break
        signal = output

    return signal


def part2(program):
    permutations = itertools.permutations([5, 6, 7, 8, 9])

    max_output = 0
    for permutation in permutations:
        output = feedback_amplifiers(program, permutation)
        max_output = max(output, max_output)

    return max_output


class TestDay7(unittest.TestCase):
    def test_permutations(self):
        self.assertEqual(permutations([]), list(itertools.permutations([])))
        self.assertEqual(
            permutations([0, 1, 2, 3, 4]), list(itertools.permutations([0, 1, 2, 3, 4]))
        )

    def test_part1(self):
        self.assertEqual(
            amplifiers(
                parse("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"), [4, 3, 2, 1, 0]
            ),
            43210,
        )

        self.assertEqual(
            amplifiers(
                parse(
                    "3,23,3,24,1002,24,10,24,1002,23,-1,23,"
                    "101,5,23,23,1,24,23,23,4,23,99,0,0"
                ),
                [0, 1, 2, 3, 4],
            ),
            54321,
        )

        self.assertEqual(
            amplifiers(
                parse(
                    "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,"
                    "1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"
                ),
                [1, 0, 4, 3, 2],
            ),
            65210,
        )

    def test_part2(self):
        self.assertEqual(
            feedback_amplifiers(
                parse(
                    "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,"
                    "27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"
                ),
                [9, 8, 7, 6, 5],
            ),
            139629729,
        )

        self.assertEqual(
            feedback_amplifiers(
                parse(
                    "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,"
                    "-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,"
                    "53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"
                ),
                [9, 7, 8, 5, 6],
            ),
            18216,
        )


if __name__ == "__main__":
    unittest.main(exit=False)

    with open("../inputs/day7.input") as f:
        program = f.readline()

    print(part1(parse(program)))  # 92663
    print(part2(parse(program)))  # 14365052
