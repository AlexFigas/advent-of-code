def simulate_guard_path(file_path):
    grid = parse_input(file_path)

    # Directions: up, right, down, left
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    direction_symbols = "^>v<"

    # Parse the grid for the starting position and initial direction
    guard_pos = None
    direction_idx = None
    for row_idx, row in enumerate(grid):
        for col_idx, char in enumerate(row):
            if char in direction_symbols:
                guard_pos = (row_idx, col_idx)
                direction_idx = direction_symbols.index(char)
                break
        if guard_pos:
            break

    visited_positions = set()
    visited_positions.add(guard_pos)

    rows, cols = len(grid), len(grid[0])

    while True:
        # Check the position in front of the guard
        delta = directions[direction_idx]
        new_pos = (guard_pos[0] + delta[0], guard_pos[1] + delta[1])

        # If the guard moves out of bounds, stop
        if new_pos[0] < 0 or new_pos[0] >= rows or new_pos[1] < 0 or new_pos[1] >= cols:
            break

        # Check if the new position is blocked
        if grid[new_pos[0]][new_pos[1]] == "#":
            # Turn right
            direction_idx = (direction_idx + 1) % 4
        else:
            # Move forward
            guard_pos = new_pos
            visited_positions.add(guard_pos)

    return len(visited_positions)


def parse_input(file_path):
    with open(file_path) as f:
        return [line.strip() for line in f]


print(simulate_guard_path("input/day6_test.txt"))  # Expected: 41
print(simulate_guard_path("input/day6.txt"))
