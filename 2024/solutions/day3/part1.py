import re


def parse_and_compute(memory):
    # Regex pattern to match valid mul(X,Y) instructions
    pattern = r"mul\((\d+),(\d+)\)"

    # Find all matches
    matches = re.findall(pattern, memory)

    # Compute the sum of products
    total = 0
    for x, y in matches:
        total += int(x) * int(y)

    return total


def parse_input(file_path):
    with open(file_path, "r") as file:
        memory = file.read()
    return memory


if __name__ == "__main__":
    memory = parse_input("./input/day3.txt")
    result = parse_and_compute(memory)
    print("Sum of valid mul(X,Y) results:", result)
