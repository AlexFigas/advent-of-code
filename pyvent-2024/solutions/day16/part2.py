import numpy as np
import heapq
from collections import deque

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def parse_input(lines):
    grid = np.array([list(row) for row in lines])
    height, width = grid.shape

    start = tuple(np.argwhere(grid == "S")[0])
    end = tuple(np.argwhere(grid == "E")[0])

    return grid, height, width, start, end


def bfs(grid, height, width, start, end):
    # Initialize priority queue with the start state
    pq = [(0, (start, 1))]  # (cost, ((x, y), direction))
    visited = {(start, 1): 0}

    while pq:
        cost, ((x, y), direction) = heapq.heappop(pq)

        # Skip if this state has already been processed with a lower cost
        if visited.get(((x, y), direction), float("inf")) < cost:
            continue

        # Move forward
        dx, dy = DIRECTIONS[direction]
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < height and 0 <= new_y < width and grid[new_x, new_y] != "#":
            new_cost = cost + 1
            next_state = ((new_x, new_y), direction)
            if new_cost < visited.get(next_state, float("inf")):
                visited[next_state] = new_cost
                heapq.heappush(pq, (new_cost, next_state))

        # Turn left or right
        for new_direction in [(direction - 1) % 4, (direction + 1) % 4]:
            new_cost = cost + 1000  # Turning costs 1000
            next_state = ((x, y), new_direction)
            if new_cost < visited.get(next_state, float("inf")):
                visited[next_state] = new_cost
                heapq.heappush(pq, (new_cost, next_state))

    return visited, end


def solve_reindeer_maze(grid, height, width, start, end):
    visited, end_point = bfs(grid, height, width, start, end)

    min_end_cost = min(visited.get((end_point, d), float("inf")) for d in range(4))

    # Backtrack the shortest path
    on_shortest_path = set()
    q = deque()

    # Add all end states with the minimum cost to the queue
    for d in range(4):
        end_state = (end_point, d)
        if end_state in visited and visited[end_state] == min_end_cost:
            on_shortest_path.add(end_state)
            q.append(end_state)

    while q:
        (x, y), direction = q.popleft()
        current_cost = visited[((x, y), direction)]

        # Backtrack for forward moves
        dx, dy = DIRECTIONS[direction]
        prev_x, prev_y = x - dx, y - dy
        if 0 <= prev_x < height and 0 <= prev_y < width and grid[prev_x, prev_y] != "#":
            prev_cost = current_cost - 1
            prev_state = ((prev_x, prev_y), direction)
            if (
                prev_cost == visited.get(prev_state, float("inf"))
                and prev_state not in on_shortest_path
            ):
                on_shortest_path.add(prev_state)
                q.append(prev_state)

        # Backtrack for turns
        turn_cost = current_cost - 1000
        if turn_cost >= 0:
            for prev_direction in [(direction - 1) % 4, (direction + 1) % 4]:
                prev_state = ((x, y), prev_direction)
                if (
                    prev_state in visited
                    and visited[prev_state] == turn_cost
                    and prev_state not in on_shortest_path
                ):
                    on_shortest_path.add(prev_state)
                    q.append(prev_state)

    # Return the number of unique tiles on the shortest path
    return len({(x, y) for ((x, y), d) in on_shortest_path})


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

with open("input/day16.txt") as f:
    lines = f.read().splitlines()

print(solve_reindeer_maze(*parse_input(lines)))
