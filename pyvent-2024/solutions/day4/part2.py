def parse_input(file_path):
    with open(file_path, "r") as file:
        grid = [line.strip() for line in file]
    return grid


def count_xmas_patterns(grid):
    rows, cols = len(grid), len(grid[0])
    total_count = 0

    # Define the "MAS" patterns (forward and backward)
    mas_patterns = [("M", "A", "S"), ("S", "A", "M")]

    def is_xmas_center(r, c):
        for mas1 in mas_patterns:
            for mas2 in mas_patterns:
                # Top-left to bottom-right diagonal
                if (
                    0 <= r - 1 < rows
                    and 0 <= c - 1 < cols
                    and 0 <= r + 1 < rows
                    and 0 <= c + 1 < cols
                    and grid[r - 1][c - 1] == mas1[0]
                    and grid[r][c] == mas1[1]  # Top-left M/S
                    and grid[r + 1][c + 1] == mas1[2]  # Center A
                    and grid[r - 1][c + 1] == mas2[0]  # Bottom-right S/M
                    and grid[r + 1][c - 1]  # Top-right M/S
                    == mas2[2]  # Bottom-left S/M
                ):
                    return True
        return False

    # Iterate through each cell in the grid
    for r in range(rows):
        for c in range(cols):
            if is_xmas_center(r, c):
                total_count += 1

    return total_count


if __name__ == "__main__":
    grid = parse_input("./input/day4.txt")
    result = count_xmas_patterns(grid)
    print(f"Total occurrences of X-MAS patterns: {result}")
