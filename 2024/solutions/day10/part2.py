def parse_input(file_path):
    with open(file_path) as file:
        input_data = file.read()
    return [list(map(int, line.strip())) for line in input_data.strip().split("\n")]


def find_trailheads(grid):
    trailheads = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 0:
                trailheads.append((r, c))
    return trailheads


def get_neighbors(r, c, grid):
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
            neighbors.append((nr, nc))
    return neighbors


def count_distinct_trails(grid, start, memo):
    r, c = start
    if (r, c) in memo:
        return memo[(r, c)]

    # If this position is a 9, it's the end of a trail
    if grid[r][c] == 9:
        return 1

    total_trails = 0
    for nr, nc in get_neighbors(r, c, grid):
        if grid[nr][nc] == grid[r][c] + 1:
            total_trails += count_distinct_trails(grid, (nr, nc), memo)

    memo[(r, c)] = total_trails
    return total_trails


def calculate_total_rating(grid):
    trailheads = find_trailheads(grid)
    memo = {}
    total_rating = 0
    for trailhead in trailheads:
        total_rating += count_distinct_trails(grid, trailhead, memo)
    return total_rating


if __name__ == "__main__":
    grid = parse_input("input/day10.txt")
    total_rating = calculate_total_rating(grid)
    print(f"Total Rating: {total_rating}")
