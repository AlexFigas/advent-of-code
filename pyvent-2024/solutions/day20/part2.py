from collections import deque


def parse_input(file_path):
    with open(file_path, "r") as file:
        lines = file.read().splitlines()
    racetrack = [list(line) for line in lines]
    start, end = None, None
    for y, row in enumerate(racetrack):
        for x, char in enumerate(row):
            if char == "S":
                start = (x, y)
            elif char == "E":
                end = (x, y)
    return racetrack, start, end


def bfs_shortest_path(racetrack, start):
    rows, cols = len(racetrack), len(racetrack[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    queue = deque([(start[0], start[1], 0)])  # (x, y, distance)
    distances = {}

    while queue:
        x, y, dist = queue.popleft()
        if (x, y) in distances:
            continue
        distances[(x, y)] = dist

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < cols
                and 0 <= ny < rows
                and racetrack[ny][nx] != "#"
                and (nx, ny) not in distances
            ):
                queue.append((nx, ny, dist + 1))

    return distances


def count_cheats_saving_at_least(racetrack, start, end, min_saving):
    from_start = bfs_shortest_path(racetrack, start)
    from_end = bfs_shortest_path(racetrack, end)

    target_distance = from_start.get(end, float("inf")) - min_saving
    count = 0

    for (x1, y1), start_dist in from_start.items():
        for (x2, y2), end_dist in from_end.items():
            manhattan_dist = abs(x2 - x1) + abs(y2 - y1)
            if (
                manhattan_dist <= 20
                and start_dist + manhattan_dist + end_dist <= target_distance
            ):
                count += 1

    return count


if __name__ == "__main__":
    racetrack, start, end = parse_input("input/day20.txt")
    result = count_cheats_saving_at_least(racetrack, start, end, 100)
    print(f"Number of cheats saving at least 100 picoseconds: {result}")
