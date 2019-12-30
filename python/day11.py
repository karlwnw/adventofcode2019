from day5 import parse
from intcode import IntCode

BLACK = 0
WHITE = 1

N = 1j
LEFT, RIGHT = -1j, 1j


def loop_run(program, current_color=BLACK):
    heading = N
    position = 0
    painted_panels = {position: current_color}

    intcode = IntCode(program)

    while current_color is not None:
        input_value = current_color
        current_color = intcode.run(input_value)
        direction_value = intcode.run(input_value)

        if direction_value is None:
            break

        painted_panels[position] = current_color

        if direction_value not in (0, 1):
            raise RuntimeError("Invalid direction value: {}".format(direction_value))

        heading = RIGHT * heading if direction_value else LEFT * heading
        position = position + heading
        current_color = painted_panels.get(position, BLACK)

        # print(f"direction={direction_value} color={current_color}")

    return painted_panels


def print_image(panel, color=WHITE):
    values = list(panel.keys())
    x_values = [c.real for c in values]
    y_values = [c.imag for c in values]
    max_width, min_width = max(x_values), min(x_values)
    max_height, min_height = max(y_values), min(y_values)
    width, height = int(max_width - min_width) + 1, int(max_height - min_height)
    print(width, height)

    # Reverse the axes
    for y in range(height, -1, -1):
        for x in range(width, 0, -1):
            position = x + min_width + 1j * y + (min_height * 1j)
            c = panel.get(position)
            e = "##" if c == color else "  "
            end = "\n" if (x + 1) % width == 0 else ""
            print(e, end=end)


if __name__ == "__main__":
    with open("../inputs/day11.input") as f:
        program = f.readline().strip()

    # Part I
    loop_run(parse(program), BLACK)  # 2238

    # Part II
    panel = loop_run(parse(program), WHITE)
    print_image(panel)  # PKFPAZRP
