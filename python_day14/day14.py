#!/usr/bin/env python3

def datareader(filename: str, translate=str):
    with open(filename, 'r') as file:
        for line in file:
            yield translate(line.strip())


def split_lines(string: str) -> list[tuple[int, int]]:
    pairs = string.split('->')
    output_pairs = []
    for pair in pairs:
        pair_points = pair.split(',')
        output_pairs.append((int(pair_points[0]), int(pair_points[1])))
    return output_pairs


box = {"min_x": None, "max_x": None, "min_y": None, "max_y": None}


def check_bound_box(x, y):
    if box['min_x'] is None:
        box['min_x'] = box['max_x'] = data_x
    if box['min_y'] is None:
        box['min_y'] = box['max_y'] = data_y
    box['min_x'] = min([box['min_x'], x])
    box['min_y'] = min([box['min_y'], y])
    box['max_x'] = max([box['max_x'], x])
    box['max_y'] = max([box['max_y'], y])


occupied_points = set([])

starting_point = (500, 0)


def get_points_between(start_point, next_point):
    points = []
    diff_x, diff_y = (start_point[0] - next_point[0],
                      start_point[1] - next_point[1])
    if diff_x != 0 and diff_y != 0:
        print("Don't know how to do this direction")
        return points
    if diff_x != 0:
        direction = 1 if diff_x < 0 else -1
        print(start_point[0], next_point[0], direction)
        for point_x in range(start_point[0], next_point[0] + direction, direction):
            points.append((point_x, start_point[1]))
    elif diff_y != 0:
        direction = 1 if diff_y < 0 else -1
        for point_y in range(start_point[1], next_point[1] + direction, direction):
            points.append((start_point[0], point_y))
    print(f"points found {points}")
    return points


def populate_lines(line_points, occupied_points):
    start_point = line_points.pop()
    occupied_points |= set([(start_point[0], start_point[1])])
    while len(line_points):
        next_point = line_points.pop()
        points = get_points_between(start_point, next_point)
        # print(f"adding points  {points} as {set(points)} to {occupied_points}")
        occupied_points |= set(points)

        start_point = next_point
    # print(f"populated with points {occupied_points}")


for data in (datareader("../day14.txt", split_lines)):
    line_points = []
    for data_x, data_y in data:
        print(data_x, data_y)
        check_bound_box(data_x, data_y)
        line_points.append((data_x, data_y))
    print(line_points)
    populate_lines(line_points, occupied_points)

# adding infinite floow
y = box['max_y'] + 2
populate_lines(
    [(box['min_x'] - 500, y), (box['max_x'] + 500, y)], occupied_points)


def check_sand_outside_box(sand_position, box):
    if not (box['min_x'] <= sand_position[0] <= box['max_x']):
        print(f"We are outside box with {sand_position} box: {box}")
        return True
    if not (0 <= sand_position[1] <= box['max_y']):
        print(f"We are outside box with {sand_position} box: {box}")
        return True
    return False


def check_sand_point(sand_position, occupied_points):
    # We move down if possible, if it is occupied, we move down and left
    #  if that is not possible, we try down and right
    #  if that is not possible, we stop and go at rest

    if (sand_position[0], sand_position[1] + 1) not in occupied_points:
        # print("next point is available")
        return (sand_position[0], sand_position[1] + 1)
    if (sand_position[0] - 1, sand_position[1] + 1) not in occupied_points:
        # print("next point down and left is available")
        return (sand_position[0] - 1, sand_position[1] + 1)
    if (sand_position[0] + 1, sand_position[1] + 1) not in occupied_points:
        # print("next point down and right is available")
        return (sand_position[0] + 1, sand_position[1] + 1)
    print("We should stop and be at rest")
    return sand_position


print(occupied_points, len(occupied_points))
print(box)

sand_amount = 0

sand_point = None

while True:
    if not sand_point:
        print(f"picking new sand point")
        sand_point = (starting_point[0], starting_point[1])
        if sand_point in occupied_points:
            print("Can't add new sand, starting position occupied")
            break

    next_point = check_sand_point(sand_point, occupied_points)

    # print(f" sand in position {sand_point} next point {next_point}")
    # are we at rest
    if sand_point[0] == next_point[0] and sand_point[1] == next_point[1]:
        occupied_points |= set([next_point])
        # print(f"Added new point to occupied points {occupied_points}")
        sand_amount += 1
        sand_point = None
        continue
    # If we are outside box, we start to overflow
    # if check_sand_outside_box(next_point, box):
    #    break

    sand_point = next_point

print(f"full {sand_amount} moved before started to overflow")
