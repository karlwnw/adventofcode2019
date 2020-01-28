from day5 import parse, run


if __name__ == "__main__":

    with open("../inputs/day9.input") as f:
        content = f.readline().strip()

    # Part I
    print(next(run(parse(content), 1)))  # 3235019597

    # Part II
    print(next(run(parse(content), 2)))  # 80274
