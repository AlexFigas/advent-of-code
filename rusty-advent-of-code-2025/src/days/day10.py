from collections import deque
import pulp


def read_input(day):
    with open(f"inputs/day{day}.txt", "r") as f:
        return f.read().strip()


def read_test_input(day):
    with open(f"inputs/day{day}_test.txt", "r") as f:
        return f.read().strip()


def parse_line(line: str):
    # Parse [indicator] (button) ... (button) {joltage}
    indicator_end = line.find(']')
    indicator_str = line[1:indicator_end]
    indicator = [c == '#' for c in indicator_str]

    joltage_start = line.find('{')
    joltage_end = line.rfind('}')
    joltage_str = line[joltage_start + 1:joltage_end]

    buttons_str = line[indicator_end + 2 : joltage_start - 1]

    # Parse buttons: "(" x,y,z ")"
    buttons = []
    i = 0
    while i < len(buttons_str):
        if buttons_str[i] == '(':
            j = i + 1
            while j < len(buttons_str) and buttons_str[j] != ')':
                j += 1
            button_str = buttons_str[i + 1:j]
            indices = [int(x) for x in button_str.split(",") if x.strip().isdigit()]
            if indices:
                buttons.append(indices)
            i = j + 1
        else:
            i += 1

    joltage = [int(x.strip()) for x in joltage_str.split(",")]

    return indicator, buttons, joltage


# ---------- Part 1: GF(2) Gaussian Elimination ----------
def solve_part1(indicator, buttons):
    n_lights = len(indicator)
    n_buttons = len(buttons)

    if n_buttons == 0:
        return 0 if all(not x for x in indicator) else 2**32 - 1

    # Build augmented matrix
    matrix = [[0] * (n_buttons + 1) for _ in range(n_lights)]

    for b_idx, btn in enumerate(buttons):
        for light_idx in btn:
            if light_idx < n_lights:
                matrix[light_idx][b_idx] ^= 1

    for i, v in enumerate(indicator):
        matrix[i][n_buttons] = 1 if v else 0

    pivot_row = 0
    pivot_cols = []

    # Gaussian elimination
    for col in range(n_buttons):
        found = False
        for row in range(pivot_row, n_lights):
            if matrix[row][col] == 1:
                matrix[pivot_row], matrix[row] = matrix[row], matrix[pivot_row]
                found = True
                break
        if not found:
            continue

        pivot_cols.append(col)

        for row in range(n_lights):
            if row != pivot_row and matrix[row][col] == 1:
                for c in range(n_buttons + 1):
                    matrix[row][c] ^= matrix[pivot_row][c]

        pivot_row += 1

    # Inconsistency?
    for row in range(pivot_row, n_lights):
        if matrix[row][n_buttons] == 1:
            return 2**32 - 1

    is_pivot = [False] * n_buttons
    for col in pivot_cols:
        is_pivot[col] = True

    free_vars = [i for i in range(n_buttons) if not is_pivot[i]]

    min_presses = 2**32 - 1
    num_free = len(free_vars)

    limit = min(1 << num_free, 1000 if num_free > 20 else 1 << num_free)

    for combo in range(limit):
        solution = [0] * n_buttons

        # set free vars
        for idx, free_col in enumerate(free_vars):
            if combo & (1 << idx):
                solution[free_col] = 1

        # solve pivots
        for r, pivot_col in enumerate(pivot_cols):
            val = matrix[r][n_buttons]
            for j in range(n_buttons):
                if j != pivot_col:
                    val ^= (matrix[r][j] & solution[j])
            solution[pivot_col] = val

        presses = sum(solution)
        min_presses = min(min_presses, presses)

    return 0 if min_presses == 2**32 - 1 else min_presses


# ---------- Part 2: Integer Linear Programming ----------
def solve_part2(buttons, joltage):
    n_counters = len(joltage)
    n_buttons = len(buttons)

    # Create the LP problem
    prob = pulp.LpProblem("Counter_Optimization", pulp.LpMinimize)

    # Decision variables: number of times to press each button
    button_presses = [pulp.LpVariable(f"button_{i}", lowBound=0, cat='Integer') for i in range(n_buttons)]

    # Objective: minimize total button presses
    prob += pulp.lpSum(button_presses)

    # Constraints: each counter must reach its target value
    for counter_idx in range(n_counters):
        constraint = 0
        for button_idx, button in enumerate(buttons):
            if counter_idx in button:
                constraint += button_presses[button_idx]
        prob += constraint == joltage[counter_idx], f"counter_{counter_idx}"

    # Solve
    prob.solve(pulp.PULP_CBC_CMD(msg=0))

    # Check if solution exists
    if prob.status != pulp.LpStatusOptimal:
        return 2**32 - 1

    return int(pulp.value(prob.objective))


def part1(input_str):
    vals = []
    for line in input_str.splitlines():
        if line.strip():
            indicator, buttons, _ = parse_line(line)
            r = solve_part1(indicator, buttons)
            vals.append(0 if r == 2**32 - 1 else r)
    return sum(vals)


def part2(input_str):
    vals = []
    for line in input_str.splitlines():
        if line.strip():
            _, buttons, joltage = parse_line(line)
            r = solve_part2(buttons, joltage)
            vals.append(0 if r == 2**32 - 1 else r)
    return sum(vals)


# ---------- Runner ----------
def run():
    input_data = read_input(10)
    print("Part 1:", part1(input_data))
    print("Part 2:", part2(input_data))


# ---------- Tests ----------
def test_part1():
    ex = read_test_input(10)
    assert part1(ex) == 7


def test_part2():
    ex = read_test_input(10)
    assert part2(ex) == 33


if __name__ == "__main__":
    run()
