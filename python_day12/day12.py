#!/usr/bin/env python3

from functools import lru_cache
import heapq


def datareader(filename: str, translate=str) -> list[str]:
    with open(filename, "r") as fileinput:
        for dataline in fileinput:
            yield translate(dataline.strip())


def calculate_height(string: str) -> list[int]:
    return [ord(character) - ord("a") for character in list(string)]


def provide_positions(map: list[int], position_list: list[tuple[int, int]], path_length: int, target_position: tuple[int, int], visited_positions: set[tuple[int, int]]) -> list[tuple[int, int]]:
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    position = position_list[-1]
    # print(
    #     f"Checking position {position} path {path_length}, {target_position}")

    for direction in directions:
        new_point = (position[0] + direction[0], position[1] + direction[1])
        if new_point in visited_positions:
            continue
        if not (0 <= new_point[0] < len(map)):
            continue
        if not (0 <= new_point[1] < len(map[0])):
            continue
        difference = map[new_point[0]][new_point[1]] - \
            map[position[0]][position[1]]
        if difference > 1:
            continue
        # all_checked_positions[new_point] = path_length + 1
        yield [position_list[-1], new_point], path_length + 1


def find_route(data_input: list[list[int]], start_position: tuple[int, int], end_position: tuple[int, int], limit=None) -> int | None:
    paths = [(1, [start_position])]
    heapq.heapify(paths)

    path_lengths = []

    visited_positions = set(start_position,)

    while len(paths):
        # print(
        #     f"paths debug: {paths[0]} lenth {len(paths[0])} from list of {[path[0] for path in paths]}")
        length, new_positions = heapq.heappop(paths)
        # print(length)
        if new_positions[-1] == end_position:
            path_lengths.append(length-1)
            print(f"found path with lengths {path_lengths}")
            return length - 1

        if limit and length >= limit:
            print(
                f"No point searching further over {length}, faster path found as {limit}")
            return None

        # print(new_positions)
        for position, path_size in provide_positions(data_input, new_positions, length, end_position, visited_positions):
            heapq.heappush(paths, (path_size, position))
            visited_positions |= set(position, )

    return None


if __name__ == "__main__":
    data_input = [list(x) for x in datareader(
        "../day12.txt", calculate_height)]

    start_position = (0, 0)
    end_position = (0, 0)

    a_positions = []

    for row_number, row in enumerate(data_input):
        # Map S as starting point
        if -14 in row:
            start_position = (row_number, row.index(-14))
        # Map E and end_position
        if -28 in row:
            end_position = (row_number, row.index(-28))
        for column, item in enumerate(row):
            if item == 0:
                a_positions.append((row_number, column))

    print(a_positions)

    data_input[start_position[0]][start_position[1]] = 0
    data_input[end_position[0]][end_position[1]] = 25

    print(data_input, start_position, end_position)
    print(find_route(data_input, start_position, end_position))
    a_paths = []
    for position in a_positions:
        limit = min(a_paths) if len(a_paths) else None

        result = find_route(data_input, position, end_position, limit)
        if result is not None:
            a_paths.append(result)
    print(min(a_paths))
