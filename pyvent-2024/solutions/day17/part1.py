def parse_input(file_path):
    with open(file_path, "r") as file:
        lines = file.read().strip().split("\n")

    # Extract register values
    registers = [
        int(lines[0].split(": ")[1]),  # Register A
        int(lines[1].split(": ")[1]),  # Register B
        int(lines[2].split(": ")[1]),  # Register C
    ]

    # Extract program
    program = list(map(int, lines[4].split(": ")[1].split(",")))

    return registers, program


def simulate_program(registers, program):
    # Initialize the registers
    A, B, C = registers

    # Initialize instruction pointer and output
    ip = 0
    output = []

    # Define helper functions for operand value resolution
    def combo_value(op):
        if op <= 3:
            return op
        elif op == 4:
            return A
        elif op == 5:
            return B
        elif op == 6:
            return C
        else:
            raise ValueError("Invalid combo operand")

    while ip < len(program):
        opcode = program[ip]
        operand = program[ip + 1]

        if opcode == 0:  # adv: A //= 2 ** combo_value(operand)
            A //= 2 ** combo_value(operand)
        elif opcode == 1:  # bxl: B ^= literal operand
            B ^= operand
        elif opcode == 2:  # bst: B = combo_value(operand) % 8
            B = combo_value(operand) % 8
        elif opcode == 3:  # jnz: if A != 0, ip = literal operand
            if A != 0:
                ip = operand
                continue
        elif opcode == 4:  # bxc: B ^= C
            B ^= C
        elif opcode == 5:  # out: output combo_value(operand) % 8
            output.append(combo_value(operand) % 8)
        elif opcode == 6:  # bdv: B = A // 2 ** combo_value(operand)
            B = A // 2 ** combo_value(operand)
        elif opcode == 7:  # cdv: C = A // 2 ** combo_value(operand)
            C = A // 2 ** combo_value(operand)
        else:
            raise ValueError("Invalid opcode")

        # Increment instruction pointer by 2 (opcode + operand)
        ip += 2

    return ",".join(map(str, output))


# Example usage
file_path = "input/day17.txt"
registers, program = parse_input(file_path)
result = simulate_program(registers, program)
print("Output:", result)
