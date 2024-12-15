# Define a function to read input from the file
def read_input(file_path):
    with open(file_path, "r") as f:
        arr, moves = f.read().split("\n\n")
    return arr.split("\n"), moves.replace("\n", "")


# Define a function to find the robot's initial position
def find_robot_position(grid):
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[0]) - 1):
            if grid[i][j] == "@":
                return i, j


# Define a function to process the robot's movements
def move_robot(grid, moves, robot_position):
    directions = {"<": (0, -1), ">": (0, 1), "^": (-1, 0), "v": (1, 0)}
    x, y = robot_position

    for move in moves:
        dx, dy = directions[move]
        nx, ny = x + dx, y + dy

        # Move until we hit a wall
        while grid[nx][ny] != "#":
            if grid[nx][ny] == ".":
                # Move the robot and boxes if possible
                while nx != x or ny != y:
                    grid[nx][ny], grid[nx - dx][ny - dy] = (
                        grid[nx - dx][ny - dy],
                        grid[nx][ny],
                    )
                    nx, ny = nx - dx, ny - dy
                x, y = x + dx, y + dy
                break
            nx, ny = nx + dx, ny + dy

    return grid


# Define a function to calculate the sum of the boxes' GPS coordinates
def calculate_gps_sum(grid):
    total_sum = 0
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[0]) - 1):
            if grid[i][j] == "O":
                total_sum += 100 * i + j
    return total_sum


# Main function to run the program
def main():
    # Read input
    grid, moves = read_input("input/day15.txt")

    # Convert grid into a list of lists for easy manipulation
    grid = [list(row) for row in grid]

    # Find the initial position of the robot
    robot_position = find_robot_position(grid)

    # Move the robot according to the given moves
    grid = move_robot(grid, moves, robot_position)

    # Calculate and print the sum of GPS coordinates
    gps_sum = calculate_gps_sum(grid)
    print(gps_sum)


# Run the main function
if __name__ == "__main__":
    main()
