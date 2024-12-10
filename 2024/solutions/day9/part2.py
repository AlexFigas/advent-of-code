import copy


def clean_up_disk_whole_files(disk):
    used_files = set()

    for file_index in range(len(disk) - 1, 0, -1):
        file_block = disk[file_index]
        if file_block[0] != "free" and file_block not in used_files:
            used_files.add(file_block)

            # Find the first suitable free block
            for i, space in enumerate(disk):
                if i >= file_index:
                    break
                if space[0] == "free" and space[1] >= file_block[1]:
                    if space[1] == file_block[1]:
                        # Exact match, swap blocks
                        disk[i], disk[file_index] = disk[file_index], disk[i]
                    else:
                        # Place part of the free space and insert the file
                        remaining_space = space[1] - file_block[1]
                        disk[i], disk[file_index] = file_block, (
                            "free",
                            remaining_space,
                        )
                        disk.insert(i + 1, ("free", remaining_space))
                    break

    return disk


def calculate_checksum(disk):
    checksum, position = 0, 0

    for file_id, length in disk:
        if file_id != "free":
            checksum += sum(
                position * file_id for position in range(position, position + length)
            )
        position += length

    return checksum


def parse_input(file_path):
    with open(file_path) as file:
        data = file.read().strip()
        return [
            (i // 2 if i % 2 == 0 else "free", int(data[i])) for i in range(len(data))
        ]


if __name__ == "__main__":
    input_file = "input/day9.txt"
    disk = parse_input(input_file)
    ordered_disk = clean_up_disk_whole_files(copy.deepcopy(disk))
    checksum = calculate_checksum(ordered_disk)
    print("Part 2, Checksum of ordered disk:", checksum)
