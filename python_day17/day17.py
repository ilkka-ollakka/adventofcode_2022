#!/usr/bin/env python3.10

from collections import deque
import math


def datareader(filename, translator=str):
    with open(filename, 'r') as file_input:
        for line in file_input:
            yield translator(line)


def parse_directions(input_line):
    line = input_line.strip()
    pattern = list(line)
    return pattern


def calculate_highest_point(locations, offset=0):
    max_point = sorted(locations, key=lambda x: x[1])[0]
    return max_point[1] + offset


def get_starting_point(locations, shape_height):
    # 2 units from left wall, 3 units from highest point/floor
    starting_offset = (2, -3)
    return (starting_offset[0], calculate_highest_point(locations) + starting_offset[1] - shape_height)


def shape_hash(shape):
    x_sum, y_sum = 0, 0
    for point in shape:
        x_sum += point[0]
        y_sum += point[1]
    return x_sum + 10 * y_sum


def get_state_hash(occupied_locations):
    x_points = set([x[0] for x in occupied_locations])
    height_list = []
    # print(f"x_points : {x_points}")
    for x_value in x_points:
        heights = [x[1] for x in occupied_locations if x[0] == x_value]
        height_list.append(min(heights))
    minimum_value = max(height_list)
    # print(height_list)
    hash_values = [x - minimum_value for x in height_list]
    # print(hash_values)
    return hash_values


def get_shape():
    # generator to return shape after another
    shapes = deque([[(0, 0), (1, 0), (2, 0), (3, 0)],  # -
                    [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],  # +
                    [(2, 0), (2, 1), (2, 2), (1, 2), (0, 2)],  # J
                    [(0, 0), (0, 1), (0, 2), (0, 3)],  # |
                    [(0, 0), (0, 1), (1, 0), (1, 1)]  # box
                    ])
    while True:
        yield shapes[0]
        shapes.rotate(-1)


def get_point(position, offset):
    return (position[0] + offset[0], position[1] + offset[1])


def get_shape_width(shape):
    points = sorted(shape, key=lambda x: x[0])[-1]
    return points[0] + 1


def get_shape_height(shape):
    points = sorted(shape, key=lambda x: x[1])[-1]
    return points[1] + 1


def move_shape(position, shape, occupied_locations, tunnel_width, command):
    # returns new position after command
    # returns same position as given if stopped
    new_x_point = position[0]
    if command == '>':
        #print("Moving to right")
        new_x_point += 1
    else:
        #print("Moving to left")
        new_x_point -= 1
    shape_width = get_shape_width(shape)
    if new_x_point < 0 or ((new_x_point + shape_width) > tunnel_width):
        # hit side wall, keep as is
        #  print("Hit side-wall, keep as is")
        new_x_point = position[0]
    shape_coordinates = get_shape_points((new_x_point, position[1]), shape)
    if any([point in occupied_locations for point in shape_coordinates]):
        # hit other item, can't move past them
        new_x_point = position[0]
    return (new_x_point, position[1])


def move_down(position, shape, occupied_locations):
    shape_coordinates = get_shape_points(position, shape)
    if any([(point[0], point[1]+1) in occupied_locations for point in shape_coordinates]):
        # we tried move down, but can't, so we are stopped
        return position
    return (position[0], position[1] + 1)


def print_cave(occupied_locations, shape_position=None, shape=None):
    shape_points = set()

    if shape_position and shape:
        shape_points = get_shape_points(shape_position, shape)

    starting_point = calculate_highest_point(occupied_locations) - 4
    print(f"highest point {starting_point}")

    for y in range(starting_point, 1):
        print("|", end='')
        for x in range(0, 7):
            if (x, y) in shape_points:
                print("@", end='')
            elif (x, y) in occupied_locations:
                print("#", end='')
            else:
                print(".", end='')
        print("|")
    print("---------")


def get_shape_points(position, shape):
    points = []
    for shape_point in shape:
        points.append(get_point(position, shape_point))
    return set(points)


wind_sequence = deque([])
for command in datareader("../day17.txt", parse_directions):
    wind_sequence.extend(command)

tunnel_width = 7
shape_provider = get_shape()


occupied_locations = set()
for x in range(0, tunnel_width):
    point = (x, 0)
    occupied_locations |= set([point])

print(occupied_locations)
print(calculate_highest_point(occupied_locations))
print(get_starting_point(occupied_locations, 1))
part1 = 0
part2 = 0
cache = dict()
shape_hashes = get_shape()
rock_amount = 0
offset = 0
total_rocks = 1000000000000
# total_rocks = 2022
cycle_found = False
command_point = 0
while rock_amount < total_rocks:
    shape = next(shape_provider)

    position = get_starting_point(occupied_locations, get_shape_height(shape))

    if rock_amount == 2022:
        part1 = -1 * calculate_highest_point(occupied_locations, offset)
        print(f"part1 found with result {part1}")

    while True:
        # print_cave(occupied_locations, position, shape)
        next_command = wind_sequence[0]
        wind_sequence.rotate(-1)
        command_point += 1
        command_point %= len(wind_sequence)
        # print(f"command point {command_point} {len(wind_sequence)}")
        # print(f"command {next_command}")
        new_position = move_shape(
            position, shape, occupied_locations, tunnel_width, next_command)
        down_position = move_down(new_position, shape, occupied_locations)
        if new_position == down_position:
            points = get_shape_points(down_position, shape)
            # print(f"shape stopped with points {points}")
            occupied_locations |= set(points)
            break
        else:
            position = down_position
            # print(f"currently shape is in {position}")

    if not cycle_found:
        cache_key = tuple([*get_state_hash(occupied_locations),
                          shape_hash(shape), command_point])
        if cache_key in cache:
            highest_point = calculate_highest_point(occupied_locations)
            cycle_found = True
            print(
                f"cycle found in point {rock_amount} current height {highest_point} key: {cache_key}")
            print(len(cache))
            print(f"cache content: {cache[cache_key]}")

            rocks_per_cycle = rock_amount - cache[cache_key]['rock']
            print(
                f"{rock_amount} - {cache[cache_key]['rock']} = {rocks_per_cycle}")
            height_per_cycle = highest_point - cache[cache_key]['height']
            print(
                f"{highest_point} - {cache[cache_key]['height']} = {height_per_cycle}")

            remaining_rocks = total_rocks - rock_amount

            cycles_remaining = remaining_rocks // rocks_per_cycle

            print(
                f" {remaining_rocks} rocks can be jumped forward, in {cycles_remaining} cycles jumping to {(cycles_remaining * rocks_per_cycle) + rock_amount} rocks")

            rock_remainder = remaining_rocks % rocks_per_cycle
            print(f"manually need to check {rock_remainder} rocks")
            offset = height_per_cycle * cycles_remaining

            rock_amount = total_rocks - rock_remainder
            highest_point = calculate_highest_point(occupied_locations, offset)

            print(
                f"repetition cycle jumped to {rock_amount} points on height {highest_point} offset set to be {offset}")

        else:
            cache[cache_key] = {'rock': rock_amount, 'height': calculate_highest_point(
                occupied_locations)}
    rock_amount += 1


# print_cave(occupied_locations)
#
print(f"cache size {len(cache)}")
part2 = -1 * calculate_highest_point(occupied_locations, offset)
print(
    f"highes point part1= {part1}")
print(f"highest point for part2 = {part2}")
