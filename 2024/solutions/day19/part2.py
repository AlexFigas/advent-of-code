def parse_input(file_path):
    with open(file_path, "r") as file:
        content = file.read().strip()
    patterns, designs = content.split("\n\n")
    towel_patterns = patterns.split(", ")
    desired_designs = designs.split("\n")
    return towel_patterns, desired_designs


def count_ways(design, patterns, memo):
    if design in memo:  # Check memoization
        return memo[design]
    if not design:  # Base case: empty design
        return 1  # One valid way to form an empty string

    total_ways = 0
    for pattern in patterns:
        if design.startswith(pattern):
            # Recursively count ways for the rest of the design
            total_ways += count_ways(design[len(pattern) :], patterns, memo)

    memo[design] = total_ways  # Store result in memoization dictionary
    return total_ways


def count_total_arrangements(file_path):
    towel_patterns, desired_designs = parse_input(file_path)
    patterns = set(towel_patterns)  # Use set for O(1) lookup
    total_count = 0
    for design in desired_designs:
        memo = {}  # Separate memoization for each design
        total_count += count_ways(design, patterns, memo)
    return total_count


if __name__ == "__main__":
    result = count_total_arrangements("input/day19.txt")
    print("Total number of arrangements:", result)
