#!/usr/bin/env python3.10

from functools import cache
import heapq


def datareader(input_filename, translator=str):
    with open(input_filename) as fileinput:
        for line_number, line in enumerate(fileinput):
            yield translator(line_number, line)


def parse_map(line_number, input):
    line = input.strip()
    borders = set()
    wind = {'up': set(), 'down': set(), 'left': set(), 'right': set()}

    for position, item in enumerate(line):
        point = (position - 1, line_number - 1)
        match item:
            case '#':
                borders |= set([point])
            case '>':
                wind['right'] |= set([point])
            case '<':
                wind['left'] |= set([point])
            case '^':
                wind['up'] |= set([point])
            case 'v':
                wind['down'] |= set([point])
    return borders, wind


def calculate_bounds(border_points):
    x_axis = sorted(border_points, key=lambda x: x[0])
    y_axis = sorted(border_points, key=lambda x: x[1])
    x0, x1 = x_axis[0][0], x_axis[-1][0]
    y0, y1 = y_axis[0][1], y_axis[-1][1]

    return (x0, y0), (x1, y1)


def move_wind(wind_points, bounds):
    movement = {'up': (0, -1), 'down': (0, 1),
                'left': (-1, 0), 'right': (1, 0)}
    new_wind_points = dict()
    for direction in movement:
        points = wind_points[direction]
        move_amount = movement[direction]
        new_points = set([((point[0] + move_amount[0]) % bounds[1][0],
                         (point[1] + move_amount[1]) % bounds[1][1]) for point in points])

        new_wind_points[direction] = new_points
    return new_wind_points


def draw_maze(wind_points, bounds, border_points, current_position, target_point):

    for y in range(bounds[0][1], bounds[1][1]+1):
        print(f"({y:2}) ", end='')
        for x in range(bounds[0][0], bounds[1][0]+1):

            point = (x, y)

            if point == current_position:
                print('E', end='')
            elif point == target_point:
                print('@', end='')
            elif point in wind_points['up']:
                print('^', end='')
            elif point in wind_points['down']:
                print('v', end='')
            elif point in wind_points['left']:
                print('<', end='')
            elif point in wind_points['right']:
                print('>', end='')
            elif point in border_points:
                print('#', end='')
            else:
                print('.', end='')
        print('')


def check_wind_overlap(turn, wind_points, position_to_check, bounding_box, cache):
    # return True if not overlapping
    width = bounding_box[1][0]
    height = bounding_box[1][1]
    # print(width, height)

    if (turn, position_to_check) in cache:
        return cache[(turn, position_to_check)]

    key = (turn, position_to_check)

    result = True
    if (position_to_check[0], (position_to_check[1] - turn) % height) in wind_points['down']:
        result = False
    if (position_to_check[0], (position_to_check[1] + turn) % height) in wind_points['up']:
        result = False
    if ((position_to_check[0] - turn) % width, position_to_check[1]) in wind_points['right']:
        result = False
    if ((position_to_check[0] + turn) % width, position_to_check[1]) in wind_points['left']:
        result = False
    cache[key] = result
    return result


def give_possible_directions(current_position, border_points, wind_points, turn, bounding_box, cache):
    cache_key = (current_position, turn)

    if cache_key in cache:
        return cache[cache_key]

    directions = [(0, 0),  # wait
                  (1, 0),  # right
                  (0, 1),  # down
                  (-1, 0),  # left
                  (0, -1)  # up
                  ]
    possibilities = set()

    for direction in directions:
        new_point = (current_position[0] + direction[0],
                     current_position[1] + direction[1])
        if new_point in border_points:
            continue
        if not (bounding_box[0][0] <= new_point[0] <= bounding_box[1][0]):
            continue
        if not (bounding_box[0][1] <= new_point[1] <= bounding_box[1][1]):
            continue
        if check_wind_overlap(turn, wind_points, new_point, bounding_box, cache):
            possibilities.add(new_point)
    cache[cache_key] = possibilities
    return possibilities


@cache
def manhattan_distance(source, destination):
    return abs(source[0] - destination[0]) + abs(source[1] - destination[1])


def find_route(wind_points, bounding_box, border_points, current_position, target_point, turn=0):

    stack_to_follow = []
    heapq.heapify(stack_to_follow)

    heapq.heappush(stack_to_follow, (turn, manhattan_distance(current_position, target_point), current_position,
                   set([(turn, current_position)])))

    cache = set()
    wind_position_cache = dict()
    max_turn = bounding_box[1][0] * bounding_box[1][1] + turn
    print(
        f"max turn amount {max_turn} distance to goal {manhattan_distance(current_position, target_point)}")
    best_route = None
    bounding_box = calculate_bounds(border_points)
    while stack_to_follow:
        turn, distance, current_position, route_so_far = heapq.heappop(
            stack_to_follow)

        #turn = -turn

        turn += 1
        if turn >= max_turn:
            print(
                f"too many turns in this route, giving up {turn}/{max_turn} left {distance} away")
            continue

        # new_wind_points = move_wind(new_wind_points, bounding_box)

        for position in give_possible_directions(current_position, border_points, wind_points, turn, bounding_box, wind_position_cache):
            new_route = route_so_far | set([(turn, position)])
            if position == target_point:
                print(
                    f"reached target in {turn} turns taking route {sorted(new_route)}")
                max_turn = turn
                best_route = sorted(new_route)
                return turn, best_route
            if (turn, position) in cache:
                # print(
                #    f" position/time already checked {turn,current_position}")
                continue
            heapq.heappush(stack_to_follow,
                           (turn, manhattan_distance(position, target_point), position, new_route))
            cache.add((turn, position))
    return max_turn, best_route


border_points = set()
wind_points = {'up': set(), 'down': set(), 'left': set(), 'right': set()}
for border, wind in datareader('../day24.txt', parse_map):
    border_points |= border
    for direction in wind:
        wind_points[direction] |= wind[direction]

bounding_box = calculate_bounds(border_points)

# starting position top
current_position = (bounding_box[0][0] + 1, bounding_box[0][1])

target_point = (bounding_box[1][0]-1, bounding_box[1][1])

# current_position = (2, 2)
print(f"borders: {border_points}")
print(f"wind points: {wind_points}")
print(f"box {bounding_box}")
current_turn = 0
# for turn in range(0, 5):
#     print(f"turn {turn}")
#     print(f" new wind points {wind_points}")
#     draw_maze(wind_points, bounding_box, border_points, current_position)
#     wind_points = move_wind(wind_points, bounding_box)
#     print(
#         f" can move to {give_possible_directions(current_position, bounding_box, wind_points)}")
#     print("")
print(f"trying to find from {current_position} to {target_point}")
print("initial status")
draw_maze(wind_points, bounding_box, border_points,
          current_position, target_point)
result, result_route = find_route(wind_points, bounding_box, border_points,
                                  current_position, target_point)

# print("Drawing chosen route")
# new_wind = wind_points
# for turn_number, position in result_route:
#     print(f"turn: {turn_number}")
#     draw_maze(new_wind, bounding_box, border_points, position, target_point)
#     print("")
#     new_wind = move_wind(new_wind, bounding_box)

return_steps, return_route = find_route(wind_points, bounding_box, border_points,
                                        target_point, current_position, result)
return_steps, return_route = find_route(wind_points, bounding_box, border_points,
                                        current_position, target_point, return_steps)
print(f"result is {result} turns for part1")
print(f"result is {return_steps} turns for part2")
