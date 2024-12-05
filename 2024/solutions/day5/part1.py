def parse_input(file_path):
    with open(file_path, "r") as file:
        input_text = file.read()
    parts = input_text.strip().split("\n\n")
    rules = [tuple(map(int, line.split("|"))) for line in parts[0].splitlines()]
    updates = [list(map(int, line.split(","))) for line in parts[1].splitlines()]
    return rules, updates


def is_update_valid(update, rules):
    positions = {page: idx for idx, page in enumerate(update)}
    for x, y in rules:
        if x in positions and y in positions:
            if positions[x] >= positions[y]:
                return False
    return True


def find_middle(update):
    return update[len(update) // 2]


def solve(input_path):
    rules, updates = parse_input(input_path)
    valid_updates = [update for update in updates if is_update_valid(update, rules)]
    middle_pages = [find_middle(update) for update in valid_updates]
    return sum(middle_pages)


print("Test result (expected 143):", solve("input/day5_test.txt"))
print("Result:", solve("input/day5.txt"))
