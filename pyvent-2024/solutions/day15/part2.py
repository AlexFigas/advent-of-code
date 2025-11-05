# Read input from file "input/day15.txt"
with open("input/day15.txt", "r") as f:
    arr, moves = f.read().split("\n\n")

# Clean up moves string by removing line breaks
moves = moves.replace("\n", "")

# Replace characters in the warehouse map
arr = arr.replace("#", "##").replace(".", "..").replace("O", "[]").replace("@", "@.")
# Convert the map to a list of lists (grid representation)
grid = [list(i) for i in arr.split("\n")]

# Get the dimensions of the grid
n, m = len(grid), len(grid[0])

# Find the robot's initial position ('@') in the grid
robot_position = None
for i in range(1, n - 1):
    for j in range(1, m - 1):
        if grid[i][j] == "@":
            robot_position = (i, j)
            break
    if robot_position:
        break

# Define direction mappings for robot movements
directions = {"<": (0, -1), ">": (0, 1), "^": (-1, 0), "v": (1, 0)}

# Process each movement in the moves string
for move in moves:
    dx, dy = directions[move]
    to_move = [robot_position]  # Robot's initial position to move
    flag = True  # Flag to check if movement is valid

    # Attempt to move the robot and boxes
    for i, j in to_move:
        nx, ny = i + dx, j + dy
        if (nx, ny) not in to_move:
            # Check if the next position is blocked by a wall (#)
            if grid[nx][ny] == "#":
                flag = False
                break
            # Check if there's a box ('['), and push the box if necessary
            elif grid[nx][ny] == "[":
                to_move.extend([(nx, ny), (nx, ny + 1)])
            # Check if there's a box (']'), and push the box if necessary
            elif grid[nx][ny] == "]":
                to_move.extend([(nx, ny), (nx, ny - 1)])

    # If the movement is valid, update the grid
    if flag:
        for i, j in to_move[::-1]:  # Reverse to prevent conflicts during movement
            grid[i + dx][j + dy], grid[i][j] = grid[i][j], grid[i + dx][j + dy]
        # Update the robot's position
        robot_position = (robot_position[0] + dx, robot_position[1] + dy)

# Calculate the sum of GPS coordinates of all boxes ('[')
gps_sum = 0
for i in range(1, n - 1):
    for j in range(1, m - 1):
        if grid[i][j] == "[":
            gps_sum += 100 * i + j

# Print the final result
print(gps_sum)
