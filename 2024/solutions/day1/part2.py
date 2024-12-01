from collections import Counter


def parse_input(input_str):
    left_list = []
    right_list = []
    for line in input_str.split("\n"):
        if line.strip() == "":
            continue
        left, right = line.split()
        left_list.append(int(left))
        right_list.append(int(right))
    return left_list, right_list


def calculate_similarity_score(left_list, right_list):
    # Count occurrences of each number in the right list
    right_count = Counter(right_list)

    # Compute the similarity score
    similarity_score = sum(num * right_count[num] for num in left_list)
    return similarity_score


with open("./input/input_day1.txt") as f:
    input_str = f.read()

left_list, right_list = parse_input(input_str)

result = calculate_similarity_score(left_list, right_list)
print("Similarity Score:", result)
