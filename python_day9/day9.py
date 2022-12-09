#!/usr/bin/env python3

from enum import Enum
from itertools import pairwise


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


def datareader(filename: str, translate=str) -> list:
    with open(filename, "r") as fileinput:
        for dataline in fileinput:
            yield translate(dataline.strip())


def parse_data(data: list) -> (Direction, int):

    (direction, amount) = data.split()
    amount = int(amount)
    direction = check_direction(direction)
    return (direction, amount)


def check_direction(direction: str) -> Direction:
    direction_mapping = {"U": Direction.UP,
                         "D": Direction.DOWN,
                         "L": Direction.LEFT,
                         "R": Direction.RIGHT}

    return direction_mapping.get(direction, None)


def get_direction_tuple(direction: Direction) -> tuple:
    direction_mapping = {Direction.UP: (0, 1),
                         Direction.DOWN: (0, -1),
                         Direction.LEFT: (-1, 0),
                         Direction.RIGHT: (1, 0)}
    return direction_mapping.get(direction, (0, 0))


def check_tail_move(tail_position: tuple, head_position: tuple) -> tuple:
    (x_offset, y_offset) = (
        head_position[0] - tail_position[0], head_position[1] - tail_position[1])
    if abs(x_offset) <= 1 and abs(y_offset) <= 1:
        print(
            f" no need to move, staying {tail_position} head {head_position}")
        return tail_position

    # We need to move left/right
    if y_offset == 0:

        offset = 0
        if x_offset > 0:
            offset = 1
        else:
            offset = -1
        tail_position = (tail_position[0] + offset, tail_position[1])
        print(f"moving left/right {offset} to {tail_position}")
    elif x_offset == 0:
        # we need to move up/down
        offset = 0
        if y_offset > 0:
            offset = 1
        else:
            offset = -1
        tail_position = (tail_position[0], tail_position[1] + offset)
        print(f"moving up/down {offset} to {tail_position}")
    else:
        if y_offset > 0:
            y_offset = 1
        else:
            y_offset = -1
        if x_offset > 0:
            x_offset = 1
        else:
            x_offset = -1
        tail_position = (tail_position[0] +
                         x_offset, tail_position[1] + y_offset)
        print(
            f"Would need to move diagonial! to {tail_position} toward {head_position}")

    return tail_position


def move_position(head_positions: list, tail_position: tuple, input: tuple) -> tuple:
    (x, y) = get_direction_tuple(input[0])
    visited_positions = set()
    for _x in range(0, input[1]):
        first_head = head_positions[0]
        head_positions[0] = (first_head[0] + x, first_head[1] + y)
        for index_to_check in range(0, len(head_positions)-1):
            head = head_positions[index_to_check]
            tail = head_positions[index_to_check + 1]
            print(f"Checking head{index_to_check+1}")
            new_position = check_tail_move(tail, head)
            if new_position == head_positions[index_to_check + 1]:
                # no need to move, early termination
                break
            head_positions[index_to_check + 1] = new_position
        print("Cheking tail")
        tail_position = check_tail_move(tail_position, head_positions[-1])
        visited_positions |= set((tail_position,))
    return head_positions, tail_position, visited_positions


def check_knots(data: list, knots: int) -> int:

    tail_position = (0, 0)
    head_positions = [(0, 0) for x in range(knots)]

    visited_positions = set()
    print(len(head_positions))

    visited_positions |= set((tail_position,))

    for input in data:
        print(f"parsed data: {input}")
        head_positions, tail_position, new_positions = move_position(
            head_positions, tail_position, input)
        print(head_positions, tail_position)
        visited_positions |= new_positions

    print(
        f"Visited {len(visited_positions)} unique positions")
    return len(visited_positions)


if __name__ == '__main__':

    data = datareader("../day9.txt", parse_data)
    part1 = check_knots(data, 1)  # part 1
    data = datareader("../day9.txt", parse_data)
    part2 = check_knots(data, 9)  # part 2

    print(f"Part1: {part1} , Part2: {part2}")
