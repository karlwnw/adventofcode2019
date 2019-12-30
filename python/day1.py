import sys

lines = list(map(int, sys.stdin.readlines()))


def total_fuel(m):
    m = m // 3 - 2
    return m + total_fuel(m) if m > 0 else 0


# Part I
print(sum([m // 3 - 2 for m in lines]))

# Part II
print(sum([total_fuel(m) for m in lines]))
