def parse_inputs(input_str):
    inputs = {}
    for line in input_str.splitlines():
        wire, value = line.split(": ")
        inputs[wire] = int(value)
    return inputs


def sort_wire_names(wire_a, wire_b):
    return tuple(sorted([wire_a, wire_b]))


def normalize_operation(wire_a, wire_b, operation):
    sorted_wire_a, sorted_wire_b = sort_wire_names(wire_a, wire_b)
    return sorted_wire_a, sorted_wire_b, operation


def parse_operation(line):
    args, output_wire = line.split(" -> ")
    wire_a, operation, wire_b = args.split()
    return output_wire, wire_a, wire_b, operation


def parse_operations(input_str):
    operations = {}
    for line in input_str.splitlines():
        output_wire, wire_a, wire_b, operation = parse_operation(line)
        operations[output_wire] = normalize_operation(wire_a, wire_b, operation)
    return operations


def parse_input(input_str):
    inputs_str, operations_str = input_str.split("\n\n")
    return parse_inputs(inputs_str), parse_operations(operations_str)


def find_output_wire(inverted_operations, wire_a, wire_b, operation):
    return inverted_operations.get(normalize_operation(wire_a, wire_b, operation), None)


def generate_wire_name(prefix, num):
    return prefix + str(num).zfill(2)


def append_if_not_none(some_list, new_element):
    assert new_element is not None
    some_list.append(new_element)


def find_all_wires(inverted, input_num, carry_in, swapped):
    x_input = generate_wire_name("x", input_num)
    y_input = generate_wire_name("y", input_num)
    xor_output = find_output_wire(inverted, x_input, y_input, "XOR")
    and_output = find_output_wire(inverted, x_input, y_input, "AND")

    assert xor_output is not None
    assert and_output is not None

    if carry_in is not None:
        and_carry_output = find_output_wire(inverted, carry_in, xor_output, "AND")
        if not and_carry_output:
            and_output, xor_output = xor_output, and_output
            append_if_not_none(swapped, xor_output)
            append_if_not_none(swapped, and_output)
            and_carry_output = find_output_wire(inverted, carry_in, xor_output, "AND")

        xor_carry_output = find_output_wire(inverted, carry_in, xor_output, "XOR")

        if xor_output and xor_output.startswith("z"):
            xor_output, xor_carry_output = xor_carry_output, xor_output
            append_if_not_none(swapped, xor_output)
            append_if_not_none(swapped, xor_carry_output)

        if and_output and and_output.startswith("z"):
            and_output, xor_carry_output = xor_carry_output, and_output
            append_if_not_none(swapped, and_output)
            append_if_not_none(swapped, xor_carry_output)

        if and_carry_output and and_carry_output.startswith("z"):
            and_carry_output, xor_carry_output = xor_carry_output, and_carry_output
            append_if_not_none(swapped, and_carry_output)
            append_if_not_none(swapped, xor_carry_output)

        assert and_carry_output is not None
        assert and_output is not None

        carry_out = find_output_wire(inverted, and_carry_output, and_output, "OR")
    else:
        xor_carry_output = xor_output
        carry_out = and_output

    assert xor_carry_output is not None
    assert carry_out is not None
    return xor_carry_output, carry_out


def invert_operations(operations):
    inverted = {v: k for k, v in operations.items()}
    assert len(inverted) == len(operations)
    return inverted


def solve(input_str):
    _, operations = parse_input(input_str)
    inverted = invert_operations(operations)
    carry_in = None
    swapped = []

    input_size = len([wire for wire in operations if wire.startswith("z")]) - 2
    for bit_num in range(input_size):
        xor_carry_output, carry_out = find_all_wires(
            inverted, bit_num, carry_in, swapped
        )

        if (
            carry_out
            and carry_out.startswith("z")
            and carry_out != generate_wire_name("z", input_size + 1)
        ):
            carry_out, xor_carry_output = xor_carry_output, carry_out
            assert carry_out is not None
            swapped.append(carry_out)
            assert xor_carry_output is not None
            swapped.append(xor_carry_output)

        carry_in = (
            carry_out
            if carry_out
            else find_output_wire(
                inverted,
                generate_wire_name("x", bit_num),
                generate_wire_name("y", bit_num),
                "AND",
            )
        )

    return ",".join(sorted(swapped))


if __name__ == "__main__":
    with open("input/day24.txt") as f:
        input_str = f.read()
        print(solve(input_str))
