def parse_input(file_path):
    with open(file_path, "r") as file:
        grid = [line.strip() for line in file]
    return grid


def count_word_occurrences(grid, word):
    rows, cols = len(grid), len(grid[0])
    word_len = len(word)
    total_count = 0

    # Directions: (row_step, col_step)
    directions = [
        (0, 1),  # Right
        (0, -1),  # Left
        (1, 0),  # Down
        (-1, 0),  # Up
        (1, 1),  # Diagonal down-right
        (-1, -1),  # Diagonal up-left
        (1, -1),  # Diagonal down-left
        (-1, 1),  # Diagonal up-right
    ]

    def is_valid_position(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def matches_word(r, c, row_step, col_step):
        for i in range(word_len):
            nr, nc = r + i * row_step, c + i * col_step
            if not is_valid_position(nr, nc) or grid[nr][nc] != word[i]:
                return False
        return True

    # Search for the word in all directions
    for r in range(rows):
        for c in range(cols):
            for row_step, col_step in directions:
                if matches_word(r, c, row_step, col_step):
                    total_count += 1

    return total_count


if __name__ == "__main__":
    grid = parse_input("./input/day4.txt")
    word = "XMAS"
    result = count_word_occurrences(grid, word)
    print(f"Total occurrences of '{word}': {result}")
