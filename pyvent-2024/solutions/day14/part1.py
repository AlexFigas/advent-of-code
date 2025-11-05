def simulate_robots(input_data, width, height, seconds):
    # Parse input into positions and velocities
    robots = []
    for line in input_data.strip().split("\n"):
        line = line.strip()  # Remove leading/trailing whitespace
        position, velocity = line.split(" v=")
        position = position.strip()[2:]  # Remove "p=" and any spaces
        velocity = velocity.strip()
        px, py = map(int, position.split(","))
        vx, vy = map(int, velocity.split(","))
        robots.append(((px, py), (vx, vy)))

    # Simulate robots' positions after `seconds` seconds
    final_positions = []
    for (px, py), (vx, vy) in robots:
        # Compute position after `seconds` seconds with wrap-around
        final_x = (px + vx * seconds) % width
        final_y = (py + vy * seconds) % height
        final_positions.append((final_x, final_y))

    # Divide the space into quadrants
    mid_x, mid_y = width // 2, height // 2
    quadrants = [0, 0, 0, 0]  # Top-left, Top-right, Bottom-left, Bottom-right

    for x, y in final_positions:
        if x == mid_x or y == mid_y:
            continue  # Skip robots on the middle lines
        elif x < mid_x and y < mid_y:
            quadrants[0] += 1  # Top-left
        elif x >= mid_x and y < mid_y:
            quadrants[1] += 1  # Top-right
        elif x < mid_x and y >= mid_y:
            quadrants[2] += 1  # Bottom-left
        elif x >= mid_x and y >= mid_y:
            quadrants[3] += 1  # Bottom-right

    # Calculate the safety factor by multiplying quadrant counts
    safety_factor = 1
    for count in quadrants:
        safety_factor *= count

    return safety_factor


def parse_input(file_path):
    with open(file_path, "r") as f:
        return f.read()


if __name__ == "__main__":
    input_data = parse_input("input/day14.txt")

    # Space dimensions and simulation time
    width, height = 101, 103
    seconds = 100

    # Calculate and print the safety factor
    safety_factor = simulate_robots(input_data, width, height, seconds)
    print("Safety Factor:", safety_factor)
