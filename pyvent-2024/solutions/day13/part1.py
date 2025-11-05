import re
from math import gcd
from itertools import product


def parse_input(file_path):
    machines = []
    with open(file_path, "r") as f:
        content = f.read()
    # Split into individual machine definitions
    machine_blocks = content.strip().split("\n\n")

    for block in machine_blocks:
        # Parse the input using regex
        match = re.search(
            r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)",
            block,
        )
        if match:
            XA, YA, XB, YB, XP, YP = map(int, match.groups())
            machines.append((XA, YA, XB, YB, XP, YP))
    return machines


def solve_claw_machine(XA, YA, XB, YB, XP, YP):
    # Diophantine linear equation system
    # Check all combinations of A and B presses (max 100 each)
    best_cost = float("inf")
    for a, b in product(range(101), repeat=2):
        if a * XA + b * XB == XP and a * YA + b * YB == YP:
            cost = 3 * a + b
            if cost < best_cost:
                best_cost = cost
    return best_cost if best_cost != float("inf") else None


if __name__ == "__main__":
    machines = parse_input("input/day13.txt")

    total_cost = 0
    prizes_won = 0

    for machine in machines:
        XA, YA, XB, YB, XP, YP = machine
        cost = solve_claw_machine(XA, YA, XB, YB, XP, YP)
        if cost is not None:
            total_cost += cost
            prizes_won += 1

    print(f"Prizes won: {prizes_won}")
    print(f"Total cost: {total_cost}")
