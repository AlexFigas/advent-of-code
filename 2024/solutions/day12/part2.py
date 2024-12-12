import numpy as np
from collections import deque


def parse_input(input_path):
    with open(input_path) as f:
        lines = [list(row.strip()) for row in f.readlines()]
    return np.array(lines)


def on_map(x, y, height, width):
    return 0 <= x < height and 0 <= y < width


def find_plot_BFS(grid, start_x, start_y, visited):
    plant_type = grid[start_x, start_y]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
    queue = deque([(start_x, start_y)])
    visited[start_x, start_y] = True

    area = 0
    perimeter = 0
    cells = {(start_x, start_y)}

    while queue:
        x, y = queue.pop()
        area += 1

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if on_map(nx, ny, grid.shape[0], grid.shape[1]):
                if grid[nx, ny] == plant_type and not visited[nx, ny]:
                    visited[nx, ny] = True
                    queue.append((nx, ny))
                    cells.add((nx, ny))
                elif grid[nx, ny] != plant_type:
                    perimeter += 1
            else:
                perimeter += 1  # Out of bounds contributes to perimeter

    # Calculate the number of sides (== corners) for the plot
    sides = calculate_corners(cells)
    return area, perimeter, sides


def calculate_corners(cells):
    corners = 0

    for cell in cells:
        u = (cell[0] - 1, cell[1])  # Up
        d = (cell[0] + 1, cell[1])  # Down
        r = (cell[0], cell[1] + 1)  # Right
        l = (cell[0], cell[1] - 1)  # Left
        if u not in cells and r not in cells:
            corners += 1
        if r not in cells and d not in cells:
            corners += 1
        if d not in cells and l not in cells:
            corners += 1
        if l not in cells and u not in cells:
            corners += 1

        # Check for internal corners (diagonals)
        ur = (cell[0] - 1, cell[1] + 1)  # Up-Right (diagonal)
        ul = (cell[0] - 1, cell[1] - 1)  # Up-Left (diagonal)
        dr = (cell[0] + 1, cell[1] + 1)  # Down-Right (diagonal)
        dl = (cell[0] + 1, cell[1] - 1)  # Down-Left (diagonal)
        if u in cells and r in cells and ur not in cells:
            corners += 1
        if r in cells and d in cells and dr not in cells:
            corners += 1
        if d in cells and l in cells and dl not in cells:
            corners += 1
        if l in cells and u in cells and ul not in cells:
            corners += 1

    return corners


def calculate_price_area_perimeter(grid):
    total_price_sides = 0
    visited = np.zeros_like(grid, dtype=bool)

    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if not visited[x, y]:
                # Calculate area, perimeter, and sides for each plot
                area, _, sides = find_plot_BFS(grid, x, y, visited)
                total_price_sides += area * sides  # Use sides instead of perimeter

    return total_price_sides


if __name__ == "__main__":
    grid = parse_input("input/day12.txt")
    price_sides = calculate_price_area_perimeter(grid)
    print("Price when using sides:", price_sides)
