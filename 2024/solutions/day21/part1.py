import numpy as np
from functools import lru_cache
from itertools import permutations


# Keypad definitions
NUMERIC_KEYPAD = np.array(
    [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], [" ", "0", "A"]]
)

DIRECTIONAL_KEYPAD = np.array([[" ", "^", "A"], ["<", "v", ">"]])

DIRECTIONS = {(-1, 0): "^", (1, 0): "v", (0, -1): "<", (0, 1): ">"}
REVERSE_DIRECTIONS = {v: k for k, v in DIRECTIONS.items()}

START_KEY = "A"


def is_safe(x, y, num=True):
    keypad = NUMERIC_KEYPAD if num else DIRECTIONAL_KEYPAD
    return 0 <= x < len(keypad) and 0 <= y < len(keypad[0]) and keypad[x][y] != " "


@lru_cache(maxsize=None)
def all_paths(startchar, endchar, num=True):
    if startchar == endchar:
        return {"A"}

    keypad = NUMERIC_KEYPAD if num else DIRECTIONAL_KEYPAD
    start = tuple(np.argwhere(keypad == startchar)[0])
    end = tuple(np.argwhere(keypad == endchar)[0])

    dx = start[0] - end[0]
    dy = start[1] - end[1]
    path = ("v" * abs(dx) if dx < 0 else "^" * abs(dx)) + (
        "<" * abs(dy) if dy > 0 else ">" * abs(dy)
    )

    correct_paths = set()
    for perm in permutations(path):
        cur_x, cur_y = start
        valid = True
        for step in perm:
            dx, dy = REVERSE_DIRECTIONS[step]
            cur_x += dx
            cur_y += dy
            if not is_safe(cur_x, cur_y, num=num):
                valid = False
                break
        if valid:
            correct_paths.add("".join(perm) + "A")

    return correct_paths


@lru_cache(maxsize=None)
def shortest_end_path(code, depth, maxdepth):
    num = depth == 1
    total_length = 0
    startchar = START_KEY

    for char in code:
        path_options = all_paths(startchar, char, num=num)
        if depth == maxdepth:
            total_length += len(min(path_options, key=len))
        else:
            lengths = {
                shortest_end_path(path, depth + 1, maxdepth) for path in path_options
            }
            total_length += min(lengths)
        startchar = char

    return total_length


def calculate_complexity(code, maxdepth):
    numeric_part = int("".join(filter(str.isdigit, code)))
    length = shortest_end_path(code, 1, maxdepth)
    return length, numeric_part


if __name__ == "__main__":
    with open("input/day21.txt") as f:
        codes = f.read().splitlines()

    total_complexity = 0
    for code in codes:
        length, numeric_part = calculate_complexity(code, 3)
        total_complexity += length * numeric_part

    print("Total complexity:", total_complexity)
