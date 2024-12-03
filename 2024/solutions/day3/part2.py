import re


def parse_and_compute_with_conditions(memory):
    # Regex patterns for instructions
    mul_pattern = r"mul\((\d+),(\d+)\)"
    do_pattern = r"do\(\)"
    dont_pattern = r"don't\(\)"

    # Initialize state and result
    enabled = True
    total = 0

    # Split memory into tokens by searching for instructions
    instructions = re.finditer(f"{mul_pattern}|{do_pattern}|{dont_pattern}", memory)

    for match in instructions:
        if match.group(1) and match.group(2):  # mul(X,Y)
            if enabled:
                x, y = int(match.group(1)), int(match.group(2))
                total += x * y
        elif match.group() == "do()":  # do()
            enabled = True
        elif match.group() == "don't()":  # don't()
            enabled = False

    return total


def parse_input(file_path):
    with open(file_path, "r") as file:
        memory = file.read()
    return memory


if __name__ == "__main__":
    memory = parse_input("./input/day3.txt")
    result = parse_and_compute_with_conditions(memory)
    print("Sum of valid mul(X,Y) results:", result)
