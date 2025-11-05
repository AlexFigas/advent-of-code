import copy


def clean_up_disk(disk):
    compact_disk = [disk[0]]  # Start with the first block
    index_free, index_last = 1, len(disk) - 1

    while index_free <= index_last:
        free_block = disk[index_free]
        last_block = disk[index_last]

        if free_block[1] == last_block[1]:
            # Same size, swap places
            compact_disk.extend([last_block, disk[index_free + 1]])
            index_free += 2
            index_last -= 2
        elif free_block[1] > last_block[1]:
            # Free block is larger, place the file and reduce free space
            compact_disk.append(last_block)
            disk[index_free] = (free_block[0], free_block[1] - last_block[1])
            index_last -= 2
        else:
            # Free block is smaller, place part of the file and keep the remainder
            compact_disk.append((last_block[0], free_block[1]))
            disk[index_last] = (last_block[0], last_block[1] - free_block[1])
            compact_disk.append(disk[index_free + 1])
            index_free += 2

    return compact_disk


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
    compacted_disk = clean_up_disk(copy.deepcopy(disk))
    checksum = calculate_checksum(compacted_disk)
    print("Checksum of compact disk:", checksum)
