from collections import defaultdict, deque


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


def topological_sort(pages, rules):
    graph = defaultdict(list)
    in_degree = defaultdict(int)

    # Build the graph and count in-degrees
    for x, y in rules:
        if x in pages and y in pages:
            graph[x].append(y)
            in_degree[y] += 1
            in_degree.setdefault(x, 0)

    # Initialize the queue with nodes having zero in-degree
    queue = deque([page for page in pages if in_degree[page] == 0])
    sorted_pages = []

    while queue:
        node = queue.popleft()
        sorted_pages.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return sorted_pages


def find_middle(update):
    return update[len(update) // 2]


def solve(file_path):
    rules, updates = parse_input(file_path)

    invalid_updates = [
        update for update in updates if not is_update_valid(update, rules)
    ]
    corrected_middle_pages = []

    for update in invalid_updates:
        corrected_update = topological_sort(update, rules)
        corrected_middle_pages.append(find_middle(corrected_update))

    return sum(corrected_middle_pages)


print("Test result (expected 123):", solve("input/day5_test.txt"))
print("Result:", solve("input/day5.txt"))
