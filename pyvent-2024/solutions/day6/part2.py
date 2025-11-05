def simulate_with_obstruction(grid, obstruction_pos):
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

    # Create a copy of the grid and place the obstruction
    grid = [list(row) for row in grid]
    grid[obstruction_pos[0]][obstruction_pos[1]] = "#"

    visited_states = set()
    rows, cols = len(grid), len(grid[0])

    while True:
        state = (guard_pos, direction_idx)
        if state in visited_states:
            # Loop detected
            return True
        visited_states.add(state)

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

    return False  # No loop detected


def find_loop_obstructions(file_path):
    grid = parse_input(file_path)

    rows, cols = len(grid), len(grid[0])
    guard_start = None

    # Find the guard's starting position
    for row_idx, row in enumerate(grid):
        for col_idx, char in enumerate(row):
            if char in "^>v<":
                guard_start = (row_idx, col_idx)
                break
        if guard_start:
            break

    valid_obstructions = 0

    # Consider every empty space as a possible obstruction
    for row_idx in range(rows):
        for col_idx in range(cols):
            if grid[row_idx][col_idx] == "." and (row_idx, col_idx) != guard_start:
                if simulate_with_obstruction(grid, (row_idx, col_idx)):
                    valid_obstructions += 1

    return valid_obstructions


def parse_input(file_path):
    with open(file_path) as f:
        return [line.strip() for line in f]


print(find_loop_obstructions("input/day6_test.txt"))  # Expected: 6
print(find_loop_obstructions("input/day6.txt"))
