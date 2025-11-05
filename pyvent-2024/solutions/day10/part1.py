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


def trailhead_score(grid, start):
    visited = set()
    stack = [start]
    reachable_nines = set()

    while stack:
        r, c = stack.pop()
        if (r, c) in visited:
            continue
        visited.add((r, c))

        # Check if this is a 9
        if grid[r][c] == 9:
            reachable_nines.add((r, c))

        # Explore neighbors
        for nr, nc in get_neighbors(r, c, grid):
            if (nr, nc) not in visited and grid[nr][nc] == grid[r][c] + 1:
                stack.append((nr, nc))

    return len(reachable_nines)


def calculate_total_score(grid):
    trailheads = find_trailheads(grid)
    total_score = 0
    for trailhead in trailheads:
        total_score += trailhead_score(grid, trailhead)
    return total_score


if __name__ == "__main__":
    grid = parse_input("input/day10.txt")
    total_score = calculate_total_score(grid)
    print(f"Total Score: {total_score}")
