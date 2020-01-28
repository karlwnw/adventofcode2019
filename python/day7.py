import itertools

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


if __name__ == "__main__":

    with open("../inputs/day7.input") as f:
        program = f.readline()

    print(part1(parse(program)))  # 92663
    print(part2(parse(program)))  # 14365052
