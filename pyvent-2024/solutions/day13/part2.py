import re
from math import gcd
from itertools import product
from sympy import symbols, Eq, solve


def parse_input(file_path, offset=0):
    machines = []
    with open(file_path, "r") as f:
        content = f.read()
    # Split into individual machine definitions
    machine_blocks = content.strip().split("\n\n")

    for block in machine_blocks:
        match = re.search(
            r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)",
            block,
        )
        if match:
            XA, YA, XB, YB, XP, YP = map(int, match.groups())
            # Apply the offset to prize positions
            XP += offset
            YP += offset
            machines.append((XA, YA, XB, YB, XP, YP))
    return machines


def solve_claw_machine(XA, YA, XB, YB, XP, YP):
    # Diophantine linear equation system
    # Use symbolic equations to solve the problem
    a, b = symbols("a b", integer=True, nonnegative=True)
    eq1 = Eq(a * XA + b * XB, XP)
    eq2 = Eq(a * YA + b * YB, YP)

    solution = solve((eq1, eq2), (a, b), dict=True)
    best_cost = float("inf")
    for sol in solution:
        a_val = sol[a]
        b_val = sol[b]
        if a_val >= 0 and b_val >= 0:
            cost = 3 * a_val + b_val
            best_cost = min(best_cost, cost)
    return best_cost if best_cost != float("inf") else None


def main(part=1):
    # Adjust the offset for part 2
    offset = 0 if part == 1 else 10**13
    machines = parse_input("input/day13.txt", offset)

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


if __name__ == "__main__":
    print("Part 1:")
    main(part=1)

    print()

    print("Part 2:")
    main(part=2)
