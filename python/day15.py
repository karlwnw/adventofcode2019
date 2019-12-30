import curses
import json

from day5 import parse
from intcode import IntCode


SAVE_FILE = "./day15.save.json"


N, S, W, E = 1j, -1j, -1, 1  # Unit vectors
UP, DOWN, LEFT, RIGHT = 1, 2, 3, 4
directions = {UP: N, DOWN: S, LEFT: W, RIGHT: E}

PATH = "."
WALL = "#"
OXYGEN = "O"

items = {0: WALL, 1: PATH, 2: OXYGEN}

KEYS_MAP = {"z": N, "s": S, "q": W, "d": E}


def draw(win, world, position):
    win.clear()
    win.border()

    margin_x = 40
    margin_y = 25

    for x in range(-80, 80, 1):
        for y in range(-30, 40, 1):
            pos = x + y * 1j

            element = "o" if position == pos else world.get(pos)
            if element:
                win.addstr(1, 1, f"{margin_y - y}, {margin_x + x}")
                win.addstr(margin_y - y, margin_x + x, element)
    win.refresh()


def get_world():
    try:
        with open(SAVE_FILE, "r") as f:
            serialized = json.loads(f.read())
            world = {complex(key): val for key, val in serialized.items()}
    except IOError:
        world = {}
    return world


def save_world(world):
    with open(SAVE_FILE, "w") as f:
        serialized = {str(key): val for key, val in world.items()}
        f.write(json.dumps(serialized))


def navigate(program):
    screen = curses.initscr()
    screen.keypad(True)
    curses.noecho()
    curses.cbreak()

    rows = 80
    cols = 55
    window = curses.newwin(cols, rows, 3, 10)

    # Track path so that we can navigate manually
    # and keep track of the path length
    path = list()
    path_set = set()

    intcode = IntCode(program)
    position = 0
    world = get_world()

    while True:
        char = screen.getch()
        screen.clear()
        screen.refresh()

        if char == 113:
            # q, quit without saving
            break
        elif char == curses.KEY_RIGHT:
            command = RIGHT
        elif char == curses.KEY_LEFT:
            command = LEFT
        elif char == curses.KEY_UP:
            command = UP
        elif char == curses.KEY_DOWN:
            command = DOWN
        else:
            # quit and save the current state
            save_world(world)
            return

        position += directions[command]
        screen.addstr(
            2, 2, f"Position (x={int(position.real)}, y={int(position.imag)})"
        )

        output = intcode.run(command)
        world[position] = items[output]

        if output == 0:
            # cancel forward movement if hit a wall
            position -= directions[command]
        else:
            if position in path_set:
                for pos in reversed(path):
                    if pos == position:
                        break
                    rem_pos = path.pop(-1)
                    path_set.remove(rem_pos)
            else:
                path.append(position)
                path_set.add(position)
            screen.addstr(2, 30, f"Path length = {len(path)}")

        draw(window, world, position)


def neighbors(point):
    """The four neighbors (without diagonals)."""
    return point + E, point + W, point + N, point + S


def propagate():
    """Propagate oxygen on the whole path, assuming
    that we have a complete map of the world.
    """
    world = get_world()
    total = sum(1 for k in world if world[k] == PATH)
    start_pos = next(k for k in world if world[k] == OXYGEN)
    path = set()

    def fill_neighbors(positions):
        next_points = []
        for pos in positions:
            for n in neighbors(pos):
                if world.get(n) == PATH and n not in path:
                    path.add(n)
                    next_points.append(n)
        return next_points

    positions = [start_pos]
    minutes = 0
    while len(path) < total:
        positions = fill_neighbors(positions)
        minutes += 1

    return minutes


if __name__ == "__main__":
    with open("../inputs/day15.input") as f:
        program = parse(f.readline())

    # Part I
    print(navigate(program))  # 354

    # Part II
    print(propagate())  # 370
