from itertools import product


def evaluate_expression(numbers, operators):
    result = numbers[0]
    for i, op in enumerate(operators):
        if op == "+":
            result += numbers[i + 1]
        elif op == "*":
            result *= numbers[i + 1]
    return result


def is_valid_equation(test_value, numbers):
    num_operators = len(numbers) - 1
    for operators in product(["+", "*"], repeat=num_operators):
        if evaluate_expression(numbers, operators) == test_value:
            return True
    return False


def total_calibration_result(file_path):
    total = 0
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            test_value, *numbers = map(int, line.replace(":", "").split())
            if is_valid_equation(test_value, numbers):
                total += test_value
    return total


if __name__ == "__main__":
    test_result = total_calibration_result("input/day7_test.txt")
    full_result = total_calibration_result("input/day7.txt")

    print(f"Test Input Total Calibration Result: {test_result}")
    print(f"Full Input Total Calibration Result: {full_result}")
