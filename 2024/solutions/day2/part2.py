def parse_input(file_path):
    with open(file_path, "r") as file:
        reports = [list(map(int, line.split())) for line in file]
    return reports


def is_safe(report):
    # Calculate differences between adjacent levels
    diffs = [report[i + 1] - report[i] for i in range(len(report) - 1)]

    # Check if all differences are within the allowed range
    if not all(1 <= abs(diff) <= 3 for diff in diffs):
        return False

    # Check if the levels are strictly increasing or strictly decreasing
    if all(diff > 0 for diff in diffs) or all(diff < 0 for diff in diffs):
        return True

    return False


def can_be_safe_with_dampener(report):
    for i in range(len(report)):
        # Create a new report excluding the i-th level
        modified_report = report[:i] + report[i + 1 :]
        if is_safe(modified_report):
            return True
    return False


def count_safe_reports_with_dampener(reports):
    count = 0
    for report in reports:
        if is_safe(report) or can_be_safe_with_dampener(report):
            count += 1
    return count


if __name__ == "__main__":
    reports = parse_input("./input/day2.txt")
    safe_count = count_safe_reports_with_dampener(reports)
    print("Number of safe reports with dampener:", safe_count)
