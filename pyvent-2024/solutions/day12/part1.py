from collections import deque


def parse_input(input_path):
    with open(input_path, "r") as file:
        input_map = file.read()
    return [list(row) for row in input_map.strip().splitlines()]


def find_regions(grid):
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    regions = []

    def bfs(r, c, plant_type):
        queue = deque([(r, c)])
        region_cells = []
        while queue:
            x, y = queue.popleft()
            if visited[x][y]:
                continue
            visited[x][y] = True
            region_cells.append((x, y))
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < rows
                    and 0 <= ny < cols
                    and not visited[nx][ny]
                    and grid[nx][ny] == plant_type
                ):
                    queue.append((nx, ny))
        return region_cells

    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                regions.append(bfs(r, c, grid[r][c]))

    return regions


def calculate_area_and_perimeter(region, grid):
    area = len(region)
    perimeter = 0
    rows, cols = len(grid), len(grid[0])

    for r, c in region:
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dx, c + dy
            if (
                nr < 0
                or nr >= rows
                or nc < 0
                or nc >= cols
                or grid[nr][nc] != grid[r][c]
            ):
                perimeter += 1

    return area, perimeter


def calculate_total_price(input_path):
    grid = parse_input(input_path)
    regions = find_regions(grid)
    total_price = 0

    for region in regions:
        area, perimeter = calculate_area_and_perimeter(region, grid)
        total_price += area * perimeter

    return total_price


print("Total Price:", calculate_total_price("input/day12.txt"))
