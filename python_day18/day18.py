#!/usr/bin/env python3

from functools import lru_cache


def datareader(filename, translator):
    with open(filename) as inputfile:
        for line in inputfile:
            yield translator(line)


def parse_coordinates(line: str) -> tuple[int, int, int]:
    x, y, z = map(int, line.split(','))
    return x, y, z


def check_open_sides(points, point, inclusion_points) -> int:
    # check if neighbour coordinate has point
    open_sides = 2 * len(point)
    check_points = []
    for offset in [-1, 1]:
        check_points.extend([
            (point[0] + offset, point[1], point[2]),
            (point[0], point[1] + offset, point[2]),
            (point[0], point[1], point[2] + offset)])

    for check in check_points:
        if check in points:
            open_sides -= 1
        elif len(inclusion_points) and check not in inclusion_points:
            open_sides -= 1
            # print(
            #     f"point {check} originating from {point} is not within inclusion list {open_sides}")
    return open_sides


def calculate_bounding_box(points):
    x_axis = sorted(points, key=lambda x: x[0])
    y_axis = sorted(points, key=lambda x: x[1])
    z_axis = sorted(points, key=lambda x: x[2])

    x0, x1 = x_axis[0][0], x_axis[-1][0]
    y0, y1 = y_axis[0][1], y_axis[-1][1]
    z0, z1 = z_axis[0][2], z_axis[-1][2]

    return x0-1, x1+1, y0-1, y1+1, z0-1, z1+1


def flood_boundingbox(points, x0, x1, y0, y1, z0, z1):
    flooded_points = set()
    flooded_points |= set([(x0, y0, z0), (x1, y1, z1)])
    for x in range(x0, x1+1):
        for y in range(y0, y1+1):
            for z in range(z0, z1+1):
                point = (x, y, z)

                if point not in points:
                    score = check_open_sides(
                        flooded_points, point, set())
                    # we are touching flooded_point, so we are outside
                    if score < 6:
                        # print(f"adding point {point} to flooded_points")
                        flooded_points |= set([point])

    return flooded_points


points = set()
for point in datareader("../day18.txt", parse_coordinates):
    points |= set([(point)])

# print(points, len(points))


total_surface = 0
for point in points:
    total_surface += check_open_sides(points, point, set())

print(f"part 1 total surface {total_surface}")

# print(f"open points to check {open_points} {len(open_points)}")

x0, x1, y0, y1, z0, z1 = calculate_bounding_box(points)
print(f"box: {x0}-{x1}, {y0}-{y1}, {z0}-{z1}")

flooded_points = flood_boundingbox(points, x0, x1, y0, y1, z0, z1)

print(len(flooded_points))
inside_score = 0
for point in points:
    inside_score += check_open_sides(points, point, flooded_points)
print(f"part2 score {inside_score}")
