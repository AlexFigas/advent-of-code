from part1 import calculate_complexity


if __name__ == "__main__":
    with open("input/day21.txt") as f:
        codes = f.read().splitlines()

    total_complexity25 = 0
    for code in codes:
        length, numeric_part = calculate_complexity(code, 26)
        total_complexity25 += length * numeric_part

    print("Total complexity:", total_complexity25)
