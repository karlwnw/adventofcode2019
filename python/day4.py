from collections import defaultdict

start, end = 357253, 892942
num_digits = 6


def solve(start, end, strict=False):
    length = end - start
    count = 0
    for i in range(length):
        number = start + i

        previous = number % 10
        consecutives = defaultdict(int)
        for j in range(1, num_digits):
            p = 10 ** j
            digit = number // p % 10

            if digit > previous:
                break

            if previous == digit:
                consecutives[digit] += 1
            previous = digit
        else:
            if (strict and 1 in consecutives.values()) or (not strict and consecutives):
                count += 1
    return count


if __name__ == "__main__":
    # Part I
    print(solve(start, end))

    # Part II
    print(solve(start, end, strict=True))
