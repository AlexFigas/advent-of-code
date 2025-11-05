import numpy as np

def parse_schematics(lines):
    keys, locks = [], []
    for grid in lines:
        rows = grid.split('\n')
        max_length = max(len(row) for row in rows)  # Determine the maximum row length
        # Pad rows to ensure consistent length
        padded_rows = [row.ljust(max_length, '.') for row in rows]
        matrix = np.array([list(row) for row in padded_rows])
        code = (np.sum(matrix == '#', axis=0) - 1).tolist()
        if np.all(matrix[0] == '#'):
            # Lock
            locks.append(code)
        else:
            # Key
            keys.append(code)
    return locks, keys

def count_fitting_pairs(locks, keys):
    counter = 0
    for lock in locks:
        for key in keys:
            counter += all(l + k < 6 for l, k in zip(lock, key))
    return counter

if __name__ == "__main__":
    with open('input/day25.txt') as f:
        lines = f.read().split("\n\n")
    locks, keys = parse_schematics(lines)
    print("Number of possibilities", count_fitting_pairs(locks, keys))
