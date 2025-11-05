def parse_input(file_path):
    with open(file_path, "r") as file:
        codes = file.read().strip().split("\n")
    return codes


# Define the keypads
numeric_keypad = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], [None, "0", "A"]]

directional_keypad = [[None, "^", "A"], ["<", "v", ">"]]

# Define the movements
movements = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}


def find_position(keypad, target):
    for i, row in enumerate(keypad):
        for j, key in enumerate(row):
            if key == target:
                return (i, j)
    return None


def bfs(start, goal, keypad):
    from collections import deque

    queue = deque([(start, "")])
    visited = set()
    visited.add(start)

    while queue:
        (current_pos, path) = queue.popleft()
        if current_pos == goal:
            return path

        for move, (di, dj) in movements.items():
            ni, nj = current_pos[0] + di, current_pos[1] + dj
            if (
                0 <= ni < len(keypad)
                and 0 <= nj < len(keypad[0])
                and keypad[ni][nj] is not None
            ):
                next_pos = (ni, nj)
                if next_pos not in visited:
                    visited.add(next_pos)
                    queue.append((next_pos, path + move))
    return None


def get_shortest_sequence(code):
    sequence = ""
    current_pos = find_position(numeric_keypad, "A")

    for char in code:
        target_pos = find_position(numeric_keypad, char)
        path = bfs(current_pos, target_pos, numeric_keypad)
        sequence += path + "A"
        current_pos = target_pos

    return sequence


def get_directional_sequence(sequence):
    directional_sequence = ""
    current_pos = find_position(directional_keypad, "A")

    for char in sequence:
        if char == "A":
            directional_sequence += "A"
        else:
            target_pos = find_position(directional_keypad, char)
            path = bfs(current_pos, target_pos, directional_keypad)
            directional_sequence += path + "A"
            current_pos = target_pos

    return directional_sequence


def calculate_complexity(sequence, code):
    numeric_part = int(code[:-1])
    return len(sequence) * numeric_part


def main():
    file_path = "input/day21.txt"
    codes = parse_input(file_path)

    total_complexity = 0
    for code in codes:
        numeric_sequence = get_shortest_sequence(code)
        directional_sequence = get_directional_sequence(numeric_sequence)
        complexity = calculate_complexity(directional_sequence, code)
        total_complexity += complexity

    print(total_complexity)


if __name__ == "__main__":
    main()
