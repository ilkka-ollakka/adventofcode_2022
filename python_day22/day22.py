#!/usr/bin/env python3.10

from doctest import ELLIPSIS_MARKER
import re


def datareader(input_filename):
    with open(input_filename, 'r') as inputfile:
        for line in inputfile:
            yield line


maze_data, code = None, None
data = list(datareader("../day22_example.txt"))
maze_data, code = ("".join(data)).split('\n\n')

code_steps = re.findall(r'(\d+|[RL])', code)

maze_points = set()
maze_box = dict()  # dict about row containing min,max points
for line_number, line_data in enumerate(maze_data.split('\n')):
    maze_box[line_number] = {'min': None, 'max': None}
    for row_point, item in enumerate(line_data):
        if item not in [' ', '\n']:
            point = (line_number, row_point, item)
            if not maze_box[line_number]['min']:
                maze_box[line_number]['min'] = row_point
                maze_box[line_number]['max'] = row_point
            maze_box[line_number]['max'] = max(
                [row_point, maze_box[line_number]['max']])
            maze_points |= set([point])

directions = {'E': (0, 1), 'W': (0, -1), 'N': (-1, 0), 'S': (1, 0)}


def retrieve_position(point, maze):
    new_position = filter(lambda x: (x[0], x[1]) == (point[0], point[1]), maze)
    return new_position


def find_furthest_x(point, maze):
    # check y position with same x that is furtest away, to find next edge
    all_relevant_nodes = filter(lambda x: x[0] == point[0], maze)
    all_relevant_nodes = list(all_relevant_nodes)
    print(f"checking what is correct point to move {all_relevant_nodes}")
    # we should be over one end of the list
    all_relevant_nodes = sorted(all_relevant_nodes, key=lambda x: x[1])
    start_point = all_relevant_nodes[0]
    end_point = all_relevant_nodes[-1]
    print(start_point, end_point)
    if abs(start_point[1] - point[1]) > abs(end_point[1] - point[1]):
        print(f"start point should be new position {start_point}")
        return (start_point[0], start_point[1], point[2])
    print(f"end point should be new position {end_point}")
    return (end_point[0], end_point[1], point[2])


def find_furthest_y(point, maze):
    # check y position with same x that is furtest away, to find next edge
    all_relevant_nodes = filter(lambda x: x[1] == point[1], maze)
    all_relevant_nodes = list(all_relevant_nodes)
    print(f"checking what is correct point to move {all_relevant_nodes}")
    # we should be over one end of the list
    all_relevant_nodes = sorted(all_relevant_nodes, key=lambda x: x[1])
    start_point = all_relevant_nodes[0]
    end_point = all_relevant_nodes[-1]
    print(start_point, end_point)
    if abs(start_point[0] - point[0]) > abs(end_point[0] - point[0]):
        print(f"start point should be new position {start_point}")
        return (start_point[0], start_point[1], point[2])
    print(f"end point should be new position {end_point}")
    return (end_point[0], end_point[1], point[2])


def calculate_score(current_position):
    final_score = ((current_position[0] + 1) *
                   1000) + (current_position[1] + 1) * 4

    direction_score = ['E', 'S', 'W', 'N']
    final_score += direction_score.index(current_position[2])
    return final_score


def move_point(point, maze, maze_box, new_point_locators):
    # move the direction that point faces
    toward = directions[point[2]]

    new_point = (point[0] + toward[0], point[1] + toward[1], point[2])
    # print(f"moving {point} on {toward} and checking {new_point} validity")
    map_position = list(retrieve_position(new_point, maze))
    if not len(map_position):
        print(f"New point not in maze, tuning, box {maze_box}")

        if toward in [(0, 1), (0, -1)]:
            print("Moving y-line")
            mapper = new_point_locators[0]
            new_point = mapper(new_point, maze)
            print(f"new point {new_point}")
        else:
            print("Moving x-line")
            mapper = new_point_locators[1]
            new_point = mapper(new_point, maze)
            print(f"new point {new_point}")
    map_position = list(retrieve_position(new_point, maze))[0]
    # print(map_position)
    if map_position:
        if map_position[2] == '#':
            return point  # don't move, keep where we are
        else:
            return new_point  # new location
    else:
        print("Panic, no position found!")
    # all the points
    print(f"Reached end, for some reason!")
    return None


def turn_point(own_position, direction):
    directions = ['E', 'S', 'W', 'N']
    # print(f"turning point {own_position} to {direction}")
    current_direction = directions.index(own_position[2])
    if direction == "R":
        current_direction += 1
    else:
        current_direction -= 1
    current_direction %= len(directions)
    new_point = (own_position[0], own_position[1],
                 directions[current_direction])
    return new_point


maze_points = sorted(maze_points, key=lambda x: (x[0], x[1]))

# starting point
starting_point = (maze_points[0][0], maze_points[0][1], 'E')
print(maze_points, starting_point)

print("Checking movement")

current_position = starting_point

for command in code_steps:
    # print(f"executing command '{command}'")
    if command in ["R", "L"]:
        current_position = turn_point(current_position, command)
    else:
        command = int(command)
        for _ in range(command):
            current_position = move_point(
                current_position, maze_points, maze_box,
                [find_furthest_x, find_furthest_y])


print(f"end position {current_position}")
print("Calculating score")
final_score = calculate_score(current_position)

print(f"final score part 1: {final_score}")

current_position = starting_point
print(current_position)

chunk_size = 4
