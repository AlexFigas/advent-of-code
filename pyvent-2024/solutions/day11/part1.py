from collections import deque


def simulate_stones(initial_stones, blinks):
    stones = deque(initial_stones)

    for _ in range(blinks):
        next_stones = deque()

        while stones:
            stone = stones.popleft()

            if stone == 0:
                next_stones.append(1)
            elif len(str(stone)) % 2 == 0:  # Even number of digits
                mid = len(str(stone)) // 2
                left = int(str(stone)[:mid])
                right = int(str(stone)[mid:])
                next_stones.append(left)
                next_stones.append(right)
            else:
                next_stones.append(stone * 2024)

        stones = next_stones

    return len(stones)


def parse_input(file_path):
    with open(file_path, "r") as file:
        return list(map(int, file.read().strip().split()))


if __name__ == "__main__":
    initial_stones = parse_input("input/day11.txt")
    blinks = 25
    result = simulate_stones(initial_stones, blinks)
    print("Number of stones after", blinks, "blinks:", result)
