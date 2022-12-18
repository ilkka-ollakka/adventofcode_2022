#!/usr/bin/env python3


from functools import lru_cache


def datareader(filename, translator):
    with open(filename) as inputfile:
        for line in inputfile:
            yield translator(line)


def calculate_manhattan_distance(point_a: set[int, int], point_b: set[int, int]) -> int:
    distance = abs(point_a[0] - point_b[0]) + abs(point_a[1] - point_b[1])
    return distance


def parse_sensor_and_beacon(input_line):
    line = input_line.split()
    sensor = (int("".join(line[2].split("=")[1][:-1])),
              int("".join(line[3].split("=")[1][:-1])))
    beacon = (int("".join(line[8].split("=")[1][:-1])),
              int("".join(line[9].split("=")[1])))

    distance = calculate_manhattan_distance(sensor, beacon)
    return sensor, beacon, distance


def calculate_positions(sensor: tuple[int, int], distance: int, y_line: int) -> set[list[int]]:
    # finding positions on y-line where can't be anything
    positions = []
    if abs(sensor[1] - y_line) > distance:
        # print(f"sensor {sensor} with distance {distance} too far away")
        return set([])
    offset = distance - abs(sensor[1] - y_line)
    # print(f"offset {offset} for sensor {sensor} with distance {distance}")
    points = [(x, y_line)
              for x in range(sensor[0] - offset, sensor[0] + offset + 1)]
    # print(f"new points {points} {len(points)}")

    return set(points)


def create_perimeter_points(sensor, distance, max_point):
    (x, y) = sensor
    for y_level in range(y-distance, y+distance + 1):
        if not (1 <= y_level < max_point):
            continue
        offset = distance - abs(y_level - y)

        if (x + offset + 1 >= max_point) or (x - offset - 1 < 0):
            continue

        y_direction = 0
        if y > y_level:
            y_direction = -1
        elif y < y_level:
            y_direction = 1
        yield (x - offset - 1, y_level)
        yield (x + offset + 1, y_level)
        if y_direction != 0:
            yield (x - offset, y_level + y_direction)
            yield (x + offset, y_level + y_direction)


def create_perimeters(sensors, max_position):
    potential_points = set()

    for sensor, distance in sensors:
        potential_points |= set([(x, y) for x, y in create_perimeter_points(
            sensor, distance, max_position) if check_within_sensor_range(sensors, (x, y))])

    return potential_points


sensors = []
beacons = set([])
y_line = 2000000
# y_line = 10
positions = set()


for sensor, beacon, distance in datareader("../day15.txt", parse_sensor_and_beacon):
    print(sensor, beacon, distance)
    sensors.append((sensor, distance))
    beacons |= set([(beacon)])
    positions |= calculate_positions(sensor, distance, y_line)
    positions -= beacons


# print(f"sensors {sensors}")
print(f"part1: {len(positions)} positions on {y_line} where signal can't be")


def check_within_sensor_range(sensors, position):
    (x, y) = position
    for sensor, distance in sensors:
        current_distance = calculate_manhattan_distance(sensor, (x, y))
        if current_distance <= distance:
            return False

    return True


# part 2, find points that is 0..2*y_line and more than distance from each sensor
search_area = create_perimeters(sensors, y_line * 2)

print(len(search_area))

final_points = [(x, y)
                for x, y in search_area if check_within_sensor_range(sensors, (x, y))]

final_point = final_points[0]
print(f"final points {final_point}")

# final_point = list(search_area)[0]
print(
    f"part2: search area frequency {final_point[0] * 4000000 + final_point[1]}")
# print(f"beacons {beacons}")
