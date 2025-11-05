import numpy as np
from collections import deque
from scipy.ndimage import label


def initialize_grid(lines, height, width):
    grid = np.zeros((height, width), dtype=int)
    for x, y in lines:
        grid[y][x] = 1
    return grid


def is_safe(grid, x, y):
    height, width = grid.shape
    return 0 <= x < height and 0 <= y < width and grid[x][y] == 0


def bfs_shortest_path(grid, start, end):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
    queue = deque([(start, 0)])  # (current_position, steps_taken)
    visited = {start}

    while queue:
        (x, y), steps = queue.popleft()

        if (x, y) == end:
            return steps  # Return the number of steps when the end is reached

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_safe(grid, nx, ny) and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), steps + 1))

    return -1  # Return -1 if there's no path


def parse_input(input_path):
    with open(input_path) as f:
        lines = [tuple(map(int, line.split(","))) for line in f.read().splitlines()]
    return lines


if __name__ == "__main__":
    lines = parse_input("input/day18.txt")

    grid_height, grid_width, input_count = 71, 71, 1024
    grid = initialize_grid(lines[:input_count], grid_height, grid_width)

    start = (0, 0)
    end = (grid_height - 1, grid_width - 1)
    min_steps = bfs_shortest_path(grid, start, end)
    print("The minimum steps to reach the exit:", min_steps)
