#!/usr/bin/env python3

from enum import Enum


def datareader(filename: str, translate=str) -> list:
    with open(filename, "r") as fileinput:
        for dataline in fileinput:
            yield translate(dataline.strip())


def split_row(string_input: str) -> list:
    return [int(x) for x in string_input]


def column_as_row(array: list, column_number: int) -> list:
    return [x[column_number] for x in array]


def parse_data(data: list) -> list:
    tree_array = []

    for line in data:
        tree_array.append(line)

    return tree_array


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


def get_direction_vector(data_array: list, x: int, y: int, direction: Direction) -> list:
    if direction not in [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]:
        return []
    if direction in [Direction.LEFT, Direction.RIGHT]:
        if direction == Direction.LEFT:
            result = data_array[y][:x]
            result.reverse()
            return result
        return data_array[y][x+1:]
    translated_coordinates = column_as_row(data_array, x)
    if direction == Direction.UP:
        result = translated_coordinates[:y]
        result.reverse()
        return result
    return translated_coordinates[y+1:]


def find_visible_trees(data_array: list, tree_stack: list) -> list:
    for y in range(1, len(data_array)-1):
        for x in range(1, len(data_array[0])-1):
            # print(f" point {x}{y}")
            # Check if tree is highest in row
            tree_height = data_array[y][x]
            # print(f" data_line {data_array[y]} right side {right_side}")
            for direction in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
                if tree_height > max(get_direction_vector(data_array, x, y, direction)):
                    # print(
                    #     f"tree [{y}][{x}] visible right {tree_height}")
                    tree_stack.append((y, x))
                    break

    return tree_stack


def calculate_scenic_score(data_array: list, y: int, x: int) -> int:
    score = 1
    value_to_check = data_array[y][x]
    # print(f"checking point {x} {y} with value of {value_to_check}")
    for direction in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
        vector = get_direction_vector(data_array, x, y, direction)
        score_value = len(vector)
        for length, value in enumerate(vector):
            if value >= value_to_check:
                score_value = len(vector[:length+1])
                break
        # print(
        #     f"{x} {y} point direction {direction} length {score_value} vector {vector}")
        score *= score_value

    # print(f"{x} {y} final score {score}")
    return score


def calculate_visible_areas(data_array: list, tree_stack: list) -> list:
    areas = []

    # print(tree_stack)
    for tree_position in tree_stack:
        (y, x) = tree_position
        if x == 0 or x == len(data_array[0]):
            areas.append(0)
            continue
        if y == 0 or y == len(data_array):
            areas.append(0)
            continue
        score = calculate_scenic_score(data_array, y, x)
        # print(
        #     f"position {x} {y} score {score}")
        areas.append(score)

    # print(areas)

    return areas


if __name__ == '__main__':
    data = datareader("../day8.txt", split_row)
    data_array = parse_data(data)

    # print(data_array)
    # trees on the edge, always visible
    tree_stack = []

    tree_stack = find_visible_trees(data_array, tree_stack)

    for x in [0, len(data_array)]:
        for y in range(1, len(data_array[0])):
            tree_stack.append((y, x))

    for y in [0, len(data_array[0])]:
        for x in range(1, len(data_array)):
            tree_stack.append((y, x))

    # print(f"size of array: {len(data_array)} * {len(data_array[0])}")
    print(f"visible trees {len(tree_stack)}")

    visible_areas = calculate_visible_areas(data_array, tree_stack)
    print(f"Biggest visible score: {max(visible_areas)}")
    # print(f"{current_directory}")
