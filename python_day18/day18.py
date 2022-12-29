#!/usr/bin/env python3

from collections import deque
from functools import lru_cache


def datareader(filename, translator):
    with open(filename) as inputfile:
        for line in inputfile:
            yield translator(line)


def parse_coordinates(line: str) -> tuple[int, int, int]:
    x, y, z = map(int, line.split(','))
    return x, y, z


def return_touching_points(point):
    check_points = []
    for offset in [-1, 1]:
        check_points.extend([
            (point[0] + offset, point[1], point[2]),
            (point[0], point[1] + offset, point[2]),
            (point[0], point[1], point[2] + offset)])
    return check_points


def check_touching_sides(points, point) -> int:
    # check if neighbour coordinate has point
    touching_sides = 0
    check_points = return_touching_points(point)
    for check in check_points:
        if check in points:
            touching_sides += 1
    return touching_sides


def calculate_bounding_box(points):
    x_axis = sorted(points, key=lambda x: x[0])
    y_axis = sorted(points, key=lambda x: x[1])
    z_axis = sorted(points, key=lambda x: x[2])

    x0, x1 = x_axis[0][0], x_axis[-1][0]
    y0, y1 = y_axis[0][1], y_axis[-1][1]
    z0, z1 = z_axis[0][2], z_axis[-1][2]

    return x0-1, x1+1, y0-1, y1+1, z0-1, z1+1

# print each layer


def print_layout(flooded_points, points):
    x0, x1, y0, y1, z0, z1 = calculate_bounding_box(points)
    for z in range(z0, z1+1):
        for y in range(y0, y1+1):
            print(f"({z:2},{y:2}) ", end='')
            for x in range(x0, x1+1):
                point = (x, y, z)
                if point in flooded_points:
                    print("@", end='')
                elif point in points:
                    print("x", end='')
                else:
                    print(" ", end='')
            print("")
        print("\n\n")


def check_outside_box(point, x0, x1, y0, y1, z0, z1):
    if not (x0 <= point[0] <= x1):
        return True
    if not (y0 <= point[1] <= y1):
        return True
    if not (z0 <= point[2] <= z1):
        return True
    return False


def flood_boundingbox(points, x0, x1, y0, y1, z0, z1, flooded_points=set(), current_point=None):
    # furthest corner is assumed to be outside
    if current_point is None:
        current_point = (x0, y0, z0)
    points_to_check = deque(set([current_point]))
    checked_points = set()
    # we do flood fill on stack, so pop point from stack (points_to_check), if point is in points or already checked points, continue to next
    # otherwise check that we are within bounded-boxes, and mark it as flooded, add 3-axis neightbourhs to stack to check
    while len(points_to_check):
        next_point = points_to_check.pop()
        print(f"checking point {next_point}")
        if next_point in points or next_point in checked_points:
            continue
        if check_outside_box(next_point, x0, x1, y0, y1, z0, z1):
            continue
        flooded_points |= set([next_point])
        checked_points |= set([next_point])
        for point in return_touching_points(next_point):
            if point not in checked_points:
                points_to_check.append(point)

    return flooded_points


points = set()
for point in datareader("../day18.txt", parse_coordinates):
    points |= set([(point)])

# print(points, len(points))


total_surface = 0
for point in points:
    total_surface += (6-check_touching_sides(points, point))


# print(f"open points to check {open_points} {len(open_points)}")

x0, x1, y0, y1, z0, z1 = calculate_bounding_box(points)
print(f"box: {x0}-{x1}, {y0}-{y1}, {z0}-{z1}")

flooded_points = flood_boundingbox(points, x0, x1, y0, y1, z0, z1)

print_layout(flooded_points, points)

# print(len(flooded_points))
inside_score = 0
for point in points:
    inside_score += check_touching_sides(flooded_points, point)

print(f"part 1 total surface {total_surface}")
print(f"part2 score {inside_score}")
