from collections import defaultdict
from itertools import combinations


def parse_grid(lines):
    antennas = defaultdict(list)
    for y, row in enumerate(lines):
        for x, cell in enumerate(row):
            if cell != ".":  # Non-empty cells represent antennas
                antennas[cell].append((x, y))
    return antennas


def on_map(x, y, width, height):
    return 0 <= x < width and 0 <= y < height


def add_antinodes_in_direction(
    x, y, dx, dy, start, max_steps, width, height, antinodes
):
    for step in range(start, max_steps):
        ax, ay = x + step * dx, y + step * dy
        if on_map(ax, ay, width, height):
            antinodes.add((ax, ay))
        else:
            break  # Stop if out of bounds


def find_antinodes(lines):
    height = len(lines)
    width = len(lines[0])
    antinodes = set()

    antennas = parse_grid(lines)

    max_steps = 2  # Only extend up to 2 for Part 1
    start_step = 1  # Start extending from position 1

    # Iterate over each frequency and consider all pairs of antennas
    for freq, positions in antennas.items():
        for (x1, y1), (x2, y2) in combinations(positions, 2):
            dx, dy = x2 - x1, y2 - y1
            # Add antinodes in both directions for the antenna pair
            add_antinodes_in_direction(
                x1, y1, -dx, -dy, start_step, max_steps, width, height, antinodes
            )
            add_antinodes_in_direction(
                x2, y2, dx, dy, start_step, max_steps, width, height, antinodes
            )

    return len(antinodes)


if __name__ == "__main__":
    with open("input/day8.txt") as f:
        lines = f.read().splitlines()

        print("Number of unique antinodes:", find_antinodes(lines))
