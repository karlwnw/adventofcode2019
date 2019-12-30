"""
    - Load the maze as a grid (complex numbers arbitrarily, no real
      advantage here)
    - Locate the starting point
    - Find all the reachable keys from that point
    - Now we could greedily choose to fetch to closest key but
      example 2 demonstrates that it may not be optimal in the long run.
    - So let's explore all possibilities and choose the shortest: if
      we have the choice between multiple keys, we can recursively apply
      the same strategy with each key as a starting point.
    - If we naively do this, it works well for all 5 examples but it's too
      slow for our input size. At this point we can try to come up with a
      totally different strategy or think of a way to speed up our current
      code. We realize that even if we have to explore multiple branches
      their paths will meet again regardless of the order in which we collect
      the reachable keys. From example 2:

                          d
                         / ∖
              a -- b -- c    -- f
                         ∖ /
                          e

      So we can try to use memoization to only compute a sub-branch once.
      The @lru_cache decorator comes handy. We just have to make sure the
      parameters of "min_steps" can form the cache key (must be hashable +
      the collected keys must be sorted so that we can benefit from the
      cache regardless of the order in which we collect them)
"""
import unittest

from textwrap import dedent

from collections import deque
from functools import lru_cache
from string import ascii_lowercase, ascii_uppercase


N, S, W, E = 1j, -1j, -1, 1  # Unit vectors

START = "@"
PATH = "."
WALL = "#"
KEYS = ascii_lowercase
DOORS = ascii_uppercase


def bfs(graph, source):
    """Textbook Breadth-First Search implementation

    This is a quick visual reminder (not directly used here,
    see the custom BFS implementation in "reachable_keys" below)
    """
    visited = []
    queue = deque([source])
    while queue:
        source = queue.popleft()
        for child in graph[source]:
            if child not in visited:
                queue.append(child)
                visited.append(child)
    return visited


def reachable_keys(grid, source, collected_keys):
    queue = deque([source])
    keys = {}
    distances = {source: 0}

    while queue:
        source = queue.popleft()
        for child in neighbors(source):
            cell = grid[child]
            if cell == WALL:
                continue
            if child in distances:
                continue

            distances[child] = distances[source] + 1
            if cell in KEYS and cell not in collected_keys:
                keys[child] = distances[child]
            elif cell.lower() in collected_keys or cell not in DOORS:
                queue.append(child)

    return keys


def neighbors(point):
    """The four neighbors (without diagonals)."""
    return point + E, point + W, point + N, point + S


def parse(content):
    maze = {}
    starting_point = None

    for y, row in enumerate(content.split('\n')):
        for x, cell in enumerate(row):
            point = complex(x, y)
            if cell == START:
                starting_point = point
            maze[point] = cell

    return maze, starting_point


def patch_maze(maze, starting_point):
    maze[starting_point] = WALL
    maze[starting_point + N] = WALL
    maze[starting_point + S] = WALL
    maze[starting_point + E] = WALL
    maze[starting_point + W] = WALL

    starting_points = (
        starting_point + N + E,
        starting_point + N + W,
        starting_point + S + E,
        starting_point + S + W,
    )
    for p in starting_points:
        maze[p] = START

    return maze, starting_points


def parse2(content):
    maze = {}
    starting_points = []

    for y, row in enumerate(content.split('\n')):
        for x, cell in enumerate(row):
            point = complex(x, y)
            if cell == START:
                starting_points.append(point)
            maze[point] = cell

    return maze, tuple(starting_points)


def part1(grid, starting_point):

    @lru_cache(maxsize=None)
    def min_steps(starting_point, collected_keys):
        keys = reachable_keys(grid, starting_point, collected_keys)
        if not keys:
            return 0

        distances = []
        for point, dist in keys.items():
            sortedkeys = ''.join(sorted(collected_keys + grid[point]))  # Predictable order for caching param
            distances.append(dist + min_steps(point, sortedkeys))
        return min(distances)

    return min_steps(starting_point, '')


def all_reachable_keys(grid, starting_points, collected_keys):
    """For each robots, find its corresponding reachable keys"""
    all_keys = {}
    for i, point in enumerate(starting_points):
        keys = reachable_keys(grid, point, collected_keys)
        if keys:
            all_keys[i] = keys
    return all_keys


def part2(grid, starting_points):

    @lru_cache(maxsize=None)
    def min_steps(starting_points, collected_keys):
        keys = all_reachable_keys(grid, starting_points, collected_keys)
        if not keys:
            return 0

        distances = []
        for i, reachable_keys in keys.items():
            for point, dist in reachable_keys.items():
                # Explore branches one at a time:
                # For each robot, try each of its reachable keys path
                # while freezing the other robots position
                positions = tuple(point if i == j else p for j, p in enumerate(starting_points))
                sortedkeys = ''.join(sorted(collected_keys + grid[point]))
                distances.append(dist + min_steps(positions, sortedkeys))
        return min(distances)

    return min_steps(starting_points, '')


class TestDay18(unittest.TestCase):

    def test_part1_example1(self):
        content = dedent(
            """
            #########
            #b.A.@.a#
            #########
            """)
        grid, starting_point = parse(content)
        self.assertEqual(part1(grid, starting_point), 8)

    def test_part1_example2(self):
        content = dedent(
            """
            ########################
            #f.D.E.e.C.b.A.@.a.B.c.#
            ######################.#
            #d.....................#
            ########################
            """)
        grid, starting_point = parse(content)
        self.assertEqual(part1(grid, starting_point), 86)

    def test_part1_example3(self):
        content = dedent(
            """
            ########################
            #...............b.C.D.f#
            #.######################
            #.....@.a.B.c.d.A.e.F.g#
            ########################
            """)
        grid, starting_point = parse(content)
        self.assertEqual(part1(grid, starting_point), 132)

    def test_part1_example4(self):
        content = dedent(
            """
            #################
            #i.G..c...e..H.p#
            ########.########
            #j.A..b...f..D.o#
            ########@########
            #k.E..a...g..B.n#
            ########.########
            #l.F..d...h..C.m#
            #################
            """)
        grid, starting_point = parse(content)
        self.assertEqual(part1(grid, starting_point), 136)

    def test_part1_example5(self):
        content = dedent(
            """
            ########################
            #@..............ac.GI.b#
            ###d#e#f################
            ###A#B#C################
            ###g#h#i################
            ########################
            """)
        grid, starting_point = parse(content)
        self.assertEqual(part1(grid, starting_point), 81)

    def test_part2_example1(self):
        content = dedent(
            """
            #######
            #a.#Cd#
            ##@#@##
            #######
            ##@#@##
            #cB#Ab#
            #######
            """)
        grid, starting_points = parse2(content)
        self.assertEqual(part2(grid, starting_points), 8)

    def test_part2_example2(self):
        content = dedent(
            """
            ###############
            #d.ABC.#.....a#
            ######@#@######
            ###############
            ######@#@######
            #b.....#.....c#
            ###############
            """)
        grid, starting_points = parse2(content)
        self.assertEqual(part2(grid, starting_points), 24)

    def test_part2_example3(self):
        content = dedent(
            """
            #############
            #DcBa.#.GhKl#
            #.###@#@#I###
            #e#d#####j#k#
            ###C#@#@###J#
            #fEbA.#.FgHi#
            #############
            """)
        grid, starting_points = parse2(content)
        self.assertEqual(part2(grid, starting_points), 32)


if __name__ == '__main__':
    unittest.main(exit=False)

    with open("../inputs/day18.input") as f:
        grid, start = parse(f.read())

    print(part1(grid, start))  # 6316

    grid, starting_points = patch_maze(grid, start)
    print(part2(grid, starting_points))  # 1648
