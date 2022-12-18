#!/usr/bin/env python3

from itertools import zip_longest
from functools import reduce
from operator import concat
from functools import cmp_to_key
import json
import unittest


def datareader(filename: str, translate=str) -> list[str]:
    with open(filename, "r") as fileinput:
        for item in "".join(fileinput.readlines()).split("\n\n"):
            # print(f"item to split '{item}'")
            left, right = item.split("\n")[:2]
            yield json.loads(left), json.loads(right)


# returns >= 0 if in correct order, <0 if incorrect order
def compare_sides(left, right, index_position=1):
    # print(f"Checking sides {left} {right}")
    matches_indexes = set()
    match left, right:
        case int(left), int(right):
            output = right - left

            if output == 0:
                return None, None
            return output > 0, None
        case list(left), int(right):
            return compare_sides(left, [right], index_position)
        case int(left), list(right):
            return compare_sides([left], right, index_position)
        case list(left), list(right):
            # print(f"checking {left} and {right} {index_position}")
            for new_position, (new_left, new_right) in enumerate(zip_longest(left, right), start=1):
                # print(
                #     f"values: {new_left} {new_right} in positions {new_position}")
                result, output_positions = compare_sides(
                    new_left, new_right, index_position + new_position - 1)
                # print(
                #     f" position {new_position} + {index_positions} checking {new_left} and {new_right} with {result}")
                if result is None:
                    # print(f"updated positions {positions}")
                    # print(f"Match is same, continue to next item")
                    matches_indexes |= set([index_position + new_position - 1])
                    continue
                if result is not None:
                    # print(f"match result {result} case {result}")
                    return result, set(matches_indexes)

            return None, set(matches_indexes)
        case int(left), None:
            return False, None
        case None, int(right):
            return True, None
        case list(left), None:
            return False, None
        case None, list(right):
            return True, None


class TestComparators(unittest.TestCase):

    def test_first(self):
        left = [1, 1, 3, 1, 1]
        right = [1, 1, 5, 1, 1]
        self.assertTrue(compare_sides(left, right)[0])

    def test_second(self):
        left = [[1], [2, 3, 4]]
        right = [[1], 4]
        self.assertTrue(compare_sides(left, right)[0])

    def test_third(self):
        left = [9]
        right = [[8, 7, 6]]
        self.assertFalse(compare_sides(left, right)[0])

    def test_fourth(self):
        left = [[4, 4], 4, 4]
        right = [[4, 4], 4, 4, 4]
        self.assertTrue(compare_sides(left, right)[0])

    def test_fifth(self):
        left = [7, 7, 7, 7]
        right = [7, 7, 7]
        self.assertFalse(compare_sides(left, right)[0])

    def test_sixth(self):
        left = []
        right = [3]
        self.assertTrue(compare_sides(left, right)[0])

    def test_sevents(self):
        left = [[[]]]
        right = [[]]
        self.assertFalse(compare_sides(left, right)[0])

    def test_eight(self):
        left = [1, [2, [3, [4, [5, 6, 7]]]], 8, 9]
        right = [1, [2, [3, [4, [5, 6, 0]]]], 8, 9]
        self.assertFalse(compare_sides(left, right)[0])


def comparator_for_sorting(left, right):
    result, _ = compare_sides(left, right)
    print(f"comparing {left} and {right} with outcome {result}")
    if result == True:
        return 1
    if result == False:
        return -1
    return 0


if __name__ == "__main__":
    right_indexes = []
    for index, result in enumerate(datareader("../day13.txt"), start=1):
        print(f"new pair {result}")
        left = result[0]
        right = result[1]
        (result, _) = compare_sides(left, right)
        if result == True:
            right_indexes.append(index)
    print(right_indexes)
    print(f"part1 result={sum(right_indexes)}")

    all_rows = []
    for left, right in list(datareader("../day13.txt")):
        all_rows.append(left)
        all_rows.append(right)
    print("original rows")
    for row in all_rows:
        print(row)
    # Adding decode key packets
    all_rows.append([[2]])
    all_rows.append([[6]])
    sorted_data = sorted(all_rows, key=cmp_to_key(
        comparator_for_sorting), reverse=True)
    print(sorted_data)
    print("sorted rows")
    decoder_key = 1
    for position, row in enumerate(sorted_data, start=1):
        print(row)
        if row in [[[2]], [[6]]]:
            print("decoder key found")
            decoder_key *= position
    print(f"decoder key {decoder_key}")
    print(f"part2 result {decoder_key}")
    # print(
    #     f" result of compare left: {result[0]} and right: {result[1]} is: {compare_sides(result[0], result[1])}")
