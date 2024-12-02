def calculate_total_distance(left_list, right_list):
    # Sort both lists
    left_list_sorted = sorted(left_list)
    right_list_sorted = sorted(right_list)

    # Compute the total distance
    total_distance = sum(
        abs(l - r) for l, r in zip(left_list_sorted, right_list_sorted)
    )
    return total_distance


def parse_input(input_file):
    with open(input_file) as f:
        input_str = f.read()

    left_list = []
    right_list = []
    for line in input_str.split("\n"):
        if line.strip() == "":
            continue
        left, right = line.split()
        left_list.append(int(left))
        right_list.append(int(right))
    return left_list, right_list


left_list, right_list = parse_input("./input/day1.txt")
result = calculate_total_distance(left_list, right_list)
print("Total Distance:", result)
