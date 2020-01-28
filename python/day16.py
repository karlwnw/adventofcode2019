from itertools import cycle, accumulate


def parse(content):
    return list(map(int, content.strip()))


def duplicate(pattern, times):
    patterns = [pattern] * times
    output = [i for l in zip(*patterns) for i in l]
    last = output.pop(0)
    output.append(last)
    return output


def part1(numbers, phases=1):
    base_pattern = [0, 1, 0, -1]
    length = len(numbers)

    while phases > 0:
        new_pattern = []
        for i in range(1, length + 1):
            pattern = duplicate(base_pattern, i)
            # if i > 3:
            #     print(pattern)

            r = 0
            for j, n in enumerate(numbers):
                # if i > 3:
                #     print(f"{n} * {pattern[j % 4]}")
                r += n * pattern[j % len(pattern)]
            new_pattern.append(abs(r) % 10)

        phases -= 1
        numbers = new_pattern

    return numbers


def part2(numbers, iterations=100):
    """The trick is to notice the following:

    - the triangular matrix pattern (all zeroes at the bottom
      left corner)

      - which implies that the 2nd half of the output only depends
        on the 2nd half of the input, because we always multiply
        the first digits by 0.

        - the 2nd phase being "1", which makes each digit of the 2nd
          half, starting from the end equal to the accumulated sum of
          the reversed original values mod 10.
          We now have a way to quickly compute the 2nd half from the
          end.

          12345678

          8 = 8
          5 = 8 + 7 = 15 % 10
          1 = 8 + 7 + 6 = 21 % 10
          6 = 8 + 7 + 6 + 5 = 26 % 10

          2nd half = 6158

    - and with input size of 650, if we duplicate it 10000 times,
      (6,500,000) and with a 7-digit offset (5,978,261), the result
      we are looking for is close to the end of the number, hence
      in the 2nd half.

    12345678
    1*1  + 2*0  + 3*-1 + 4*0  + 5*1  + 6*0  + 7*-1 + 8*0  = 4
    1*0  + 2*1  + 3*1  + 4*0  + 5*0  + 6*-1 + 7*-1 + 8*0  = 8
    1*0  + 2*0  + 3*1  + 4*1  + 5*1  + 6*0  + 7*0  + 8*0  = 2
    1*0  + 2*0  + 3*0  + 4*1  + 5*1  + 6*1  + 7*1  + 8*0  = 2
    1*0  + 2*0  + 3*0  + 4*0  + 5*1  + 6*1  + 7*1  + 8*1  = 6
    1*0  + 2*0  + 3*0  + 4*0  + 5*0  + 6*1  + 7*1  + 8*1  = 1
    1*0  + 2*0  + 3*0  + 4*0  + 5*0  + 6*0  + 7*1  + 8*1  = 5
    1*0  + 2*0  + 3*0  + 4*0  + 5*0  + 6*0  + 7*0  + 8*1  = 8
    """
    offset = int("".join(map(str, numbers[:7])))
    size = len(numbers) * 10000 - offset
    generator = cycle(reversed(numbers))
    data = [next(generator) for _ in range(size)]
    for _ in range(iterations):
        data = [s % 10 for s in accumulate(data)]
    return "".join(str(i) for i in reversed(data[-8:]))


if __name__ == "__main__":

    with open("../inputs/day16.input") as f:
        content = f.read()

    # Part I
    print("".join(map(str, part1(parse(content), 100)[:8])))  # 27229269

    # Part II
    print(part2(parse(content), iterations=100))  # 26857164
