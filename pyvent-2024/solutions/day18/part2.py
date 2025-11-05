import numpy as np
from scipy.ndimage import label


def initialize_grid(lines, height, width):
    grid = np.zeros((height, width), dtype=int)
    for x, y in lines:
        grid[y][x] = 1
    return grid


def find_connected_components(lines, height, width):
    grid = np.zeros((height, width), dtype=int)
    structure = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])  # 4-connectivity mask

    for i, (x, y) in enumerate(lines):
        grid[y][x] = 1
        zero_mask = grid == 0

        labeled_grid, num_components = label(zero_mask, structure=structure)

        if num_components == 1:
            continue

        # Check if start and end are still connected
        if labeled_grid[0, 0] != labeled_grid[height - 1, width - 1]:
            return i, (x, y)

    return -1, (-1, -1)  # Return -1 if the path is never blocked


def parse_input(input_path):
    with open(input_path) as f:
        lines = [tuple(map(int, line.split(","))) for line in f.read().splitlines()]
    return lines


if __name__ == "__main__":
    lines = parse_input("input/day18.txt")

    grid_height, grid_width, input_count = 71, 71, 1024
    grid = initialize_grid(lines[:input_count], grid_height, grid_width)

    step, coord = find_connected_components(lines, grid_height, grid_width)
    print("The memory becomes disconnected at step:", step, "with coordinate:", coord)
