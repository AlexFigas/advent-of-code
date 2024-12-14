import matplotlib.pyplot as plt
import numpy as np

def parse_input(file_path):
    with open(file_path, 'r') as file:
        arr = [line.split() for line in file.readlines()]
    
    # Parse positions and velocities
    pos = [list(map(int, p[2:].split(","))) + list(map(int, v[2:].split(","))) for p, v in arr]
    
    return pos

def simulate_and_find_pattern(input_path):
    pos = parse_input(input_path)
    
    # Simulate for up to 10,000 steps
    for i in range(1, 10000):
        # Create a blank grid of size 101 x 103 (height x width)
        grid = np.full((101, 103), " ", dtype=str)
        
        # Update robot positions and place "#" in the grid
        for j in pos:
            j[0], j[1] = (j[0] + j[2]) % 101, (j[1] + j[3]) % 103
            grid[j[0], j[1]] = "#"
        
        # Check for the pattern "#################################" in any row
        if any("#################################" in "".join(row) for row in grid):
            print(f"Pattern found at time step {i}")
            render_grid(grid)
            break

def render_grid(grid):
    plt.imshow(np.where(grid == "#", 1, 0), cmap="Greys", origin="upper", interpolation="none")
    plt.axis('off')  # Hide axes

    plt.tight_layout()
    plt.savefig("solutions/day14/pattern.png")

# Example usage
if __name__ == "__main__":
    simulate_and_find_pattern("input/day14.txt")
