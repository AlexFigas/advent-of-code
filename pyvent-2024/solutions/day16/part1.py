from collections import deque
import heapq

# Directions: East, South, West, North
offsets = {"E": (0, 1), "S": (1, 0), "W": (0, -1), "N": (-1, 0)}
directions = ["E", "S", "W", "N"]


def parse_input(grid):
    start = None
    end = None
    maze = []

    for i, row in enumerate(grid):
        maze.append(list(row))
        for j, cell in enumerate(row):
            if cell == "S":
                start = (i, j)
            elif cell == "E":
                end = (i, j)

    return maze, start, end


def bfs(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    # Priority queue: (score, x, y, direction)
    queue = [(0, start[0], start[1], "E")]
    visited = set()

    while queue:
        score, x, y, direction = heapq.heappop(queue)

        # If we've reached the end, return the score
        if (x, y) == end:
            return score

        # Mark this state as visited
        if (x, y, direction) in visited:
            continue
        visited.add((x, y, direction))

        # Move forward
        dx, dy = offsets[direction]
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] != "#":
            heapq.heappush(queue, (score + 1, nx, ny, direction))

        # Turn left or right
        current_idx = directions.index(direction)
        left_direction = directions[(current_idx - 1) % 4]
        right_direction = directions[(current_idx + 1) % 4]

        heapq.heappush(queue, (score + 1000, x, y, left_direction))
        heapq.heappush(queue, (score + 1000, x, y, right_direction))

    return float("inf")  # If no solution found (shouldn't happen with valid input)


def solve_reindeer_maze(input_data):
    grid = input_data.strip().split("\n")
    maze, start, end = parse_input(grid)
    return bfs(maze, start, end)


# Example usage
input_data = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

with open("input/day16.txt", "r") as file:
    input_data = file.read()

print(solve_reindeer_maze(input_data))
