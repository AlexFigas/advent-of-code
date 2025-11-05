def parse_input(file_path):
    with open(file_path, "r") as file:
        content = file.read().strip()
    patterns, designs = content.split("\n\n")
    towel_patterns = patterns.split(", ")
    desired_designs = designs.split("\n")
    return towel_patterns, desired_designs


def can_construct(design, patterns, memo):
    if design in memo:  # Check memoization
        return memo[design]
    if not design:  # Base case: empty design
        return True
    for pattern in patterns:
        if design.startswith(pattern):
            # Recursively check for the rest of the design
            if can_construct(design[len(pattern) :], patterns, memo):
                memo[design] = True
                return True
    memo[design] = False  # If no pattern works
    return False


def count_possible_designs(file_path):
    towel_patterns, desired_designs = parse_input(file_path)
    patterns = set(towel_patterns)  # Use set for O(1) lookup
    memo = {}  # Memoization dictionary
    count = 0
    for design in desired_designs:
        if can_construct(design, patterns, memo):
            count += 1
    return count


if __name__ == "__main__":
    result = count_possible_designs("input/day19.txt")
    print("Number of possible designs:", result)
