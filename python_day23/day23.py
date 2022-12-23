#!/usr/bin/env python3.10


from collections import deque
from functools import lru_cache
import itertools


def datareader(filename, translator=str):
    with open(filename, 'r') as fileinput:
        for linenumber, line in enumerate(fileinput):
            yield translator(linenumber, line)


def parse_positions(linenumber, line):
    positions = set()
    for position, item in enumerate(line):
        if item == '#':
            location = (position, linenumber)
            positions |= set([location])
    # print(positions)
    return positions


@lru_cache
def give_point(point, offset):
    return (point[0] + offset[0], point[1] + offset[1])


@lru_cache
def offsets_direction(direction):
    match direction:
        case 'N':
            return [(-1, -1), (0, -1), (1, -1)]
        case 'E':
            return [(1, -1), (1, 0), (1, 1)]
        case 'S':
            return [(-1, 1), (0, 1), (1, 1)]
        case 'W':
            return [(-1, -1), (-1, 0), (-1, 1)]


def check_direction_free(position, direction, coordinates):
    offsets = offsets_direction(direction)
    points_to_check = [give_point(position, off) for off in offsets]
    # print(
    #     f"checking availability result {position} {direction} points {points_to_check}: {[point not in coordinates for point in points_to_check]}")
    return all([point not in coordinates for point in points_to_check])


def check_where_to_move(position, coordinates, round_number=0):
    directions = deque(['N', 'S', 'W', 'E'])
    directions.rotate(-round_number)
    # print(f"checking in direction {directions}")
    for direction in directions:
        if check_direction_free(position, direction, coordinates):
            # print(f"direction {direction} is selected for {position}")
            return position, direction
    # print(f"{position} can't move")
    return position, ''


def check_if_can_stay_put(position, coordinates):
    directions = ['N', 'S', 'W', 'E']
    for direction in directions:
        if not check_direction_free(position, direction, coordinates):
            return False
    # print(f"{position} can stay put")
    return True


def calculate_bounding_rectangle(elf_positions):
    x_side = sorted(elf_positions, key=lambda x: x[0])
    y_side = sorted(elf_positions, key=lambda x: x[1])
    x0, x1 = x_side[0][0], x_side[-1][0]
    y0, y1 = y_side[0][1], y_side[-1][1]
    return x0, x1, y0, y1


def print_elfs(elf_positions):
    x0, x1, y0, y1 = calculate_bounding_rectangle(elf_positions)

    for y in range(y0, y1+1):
        print(f"({x0:2},{y:2}) ", end='')
        for x in range(x0, x1+1):
            if (x, y) in elf_positions:
                print('#', end='')
            else:
                print('.', end='')
        print(f" ({x:2},{y:2})")


elf_positions = set()
for positions in datareader("../day23.txt", parse_positions):
    elf_positions |= positions

elf_positions = set(sorted(elf_positions, key=lambda x: (x[1], x[0])))
print(elf_positions)

print("Initial state")
print_elfs(elf_positions)

for round_number in itertools.count(start=0):
    print(f"Starting round {round_number + 1}")
    new_positions = []
    elfs_in_put = 0
    for elf in elf_positions:
        # print(f"checking elf in {elf}")
        if check_if_can_stay_put(elf, elf_positions):
            elfs_in_put += 1
            new_positions.append(elf)
            # print(f"elf in {elf} can stay put")
            continue
        position, direction = check_where_to_move(
            elf, elf_positions, round_number)
        if direction != '':
            new_position = give_point(
                position, offsets_direction(direction)[1])
            new_positions.append(new_position)
        else:
            new_positions.append(position)
    # print(len(elf_positions), elfs_in_put)

    # print("First half of the round done")
    # print(new_positions)
    new_points = set(set(elf_positions) & set(new_positions))
    elves_that_move = set(elf_positions) - set(new_points)
    how_many_elves_need_to_move = len(elves_that_move)
    if how_many_elves_need_to_move == 0:
        print(f"Stable state reached in round {round_number + 1}")
        break
    print(
        f"First half of the round done, moving {how_many_elves_need_to_move} elfs")
    # skipping elfs that are not moving
    for elf in elves_that_move:
        # We only have elfs that need/can move
        position, direction = check_where_to_move(
            elf, elf_positions, round_number)
        if direction != '':
            new_position = give_point(
                position, offsets_direction(direction)[1])
            if new_positions.count(new_position) != 1:
                # print(
                #     f"skipping movement, {new_position} would be crowded {new_positions.count(new_position)}")
                new_points |= set([position])
            else:
                # print(f"moving {elf} -> {new_position}")
                new_points |= set([new_position])
        else:
            new_points |= set([position])
    # elf_positions = sorted(new_points, key=lambda x: (x[1], x[0]))
    elf_positions = new_points
    # print(f"End of round {round_number + 1}")

    # print_elfs(elf_positions)
# print(elf_positions)
x0, x1, y0, y1 = calculate_bounding_rectangle(elf_positions)
area = (abs(x1-x0)+1) * (abs(y1-y0)+1)
print(
    f"calculating area={x0} {x1} {y0} {y1} = {area} filled amount = {len(elf_positions)}")
print(f"area {area} free_slots {area-len(elf_positions)}")

# print area
print_elfs(elf_positions)
