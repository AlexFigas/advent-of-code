from collections import defaultdict


def simulate_stones_optimized(initial_stones, blinks):
    # Dictionary to store the count of each stone
    stone_counts = defaultdict(int)

    # Initialize counts with the initial stones
    for stone in initial_stones:
        stone_counts[stone] += 1

    for _ in range(blinks):
        next_stone_counts = defaultdict(int)

        for stone, count in stone_counts.items():
            if stone == 0:
                next_stone_counts[1] += count
            elif len(str(stone)) % 2 == 0:  # Even number of digits
                mid = len(str(stone)) // 2
                divisor = 10**mid
                left = stone // divisor
                right = stone % divisor
                next_stone_counts[left] += count
                next_stone_counts[right] += count
            else:
                next_stone_counts[stone * 2024] += count

        stone_counts = next_stone_counts

    return sum(stone_counts.values())


def parse_input(file_path):
    with open(file_path, "r") as file:
        return list(map(int, file.read().strip().split()))


if __name__ == "__main__":
    initial_stones = parse_input("input/day11.txt")
    blinks = 75
    result = simulate_stones_optimized(initial_stones, blinks)
    print("Number of stones after", blinks, "blinks:", result)
