def parse_input(file_path):
    with open(file_path, "r") as f:
        data = f.read()

    # Split sections
    sections = data.strip().split("\n\n")

    # Parse wire values
    wire_values = {}
    for line in sections[0].strip().split("\n"):
        wire, value = line.split(": ")
        wire_values[wire] = int(value)

    # Parse gates
    gates = []
    for line in sections[1].strip().split("\n"):
        parts = line.split(" ")
        if len(parts) == 5:
            gates.append((parts[1], parts[0], parts[2], parts[4]))

    return wire_values, gates


def simulate_gates(wire_values, gates):
    unresolved_gates = gates[:]
    while unresolved_gates:
        resolved_gates = []
        for gate_type, input1, input2, output in unresolved_gates:
            if output in wire_values:
                continue  # Skip if output already has a value

            if input1 in wire_values and input2 in wire_values:
                val1 = wire_values[input1]
                val2 = wire_values[input2]

                if gate_type == "AND":
                    wire_values[output] = val1 & val2
                elif gate_type == "OR":
                    wire_values[output] = val1 | val2
                elif gate_type == "XOR":
                    wire_values[output] = val1 ^ val2

                resolved_gates.append((gate_type, input1, input2, output))

        for gate in resolved_gates:
            unresolved_gates.remove(gate)

    return wire_values


def calculate_output(wire_values):
    # Collect outputs starting with 'z' and sort by their numerical suffix
    z_outputs = {k: v for k, v in wire_values.items() if k.startswith("z")}
    sorted_bits = [v for k, v in sorted(z_outputs.items(), key=lambda x: int(x[0][1:]))]

    # Convert binary bits to decimal
    result = int(
        "".join(map(str, sorted_bits[::-1])), 2
    )  # Reverse to match LSB to MSB order
    return result


if __name__ == "__main__":
    input_path = "input/day24.txt"
    wire_values, gates = parse_input(input_path)
    wire_values = simulate_gates(wire_values, gates)
    result = calculate_output(wire_values)
    print(f"The output value is: {result}")
