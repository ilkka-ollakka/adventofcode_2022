#!/usr/bin/env python3

def datareader(filename, translate=int):
    with open(filename, "r") as fileinput:
        for dataline in fileinput:
            yield translate(dataline.strip())


def split_rows(row):
    (first, second) = row.split(',')
    (left, right) = first.split('-'), second.split('-')

    # print(left, right)

    return left, right


def contains_one_another(left, right):
    range1 = range(int(left[0]), int(left[1])+1)
    range2 = range(int(right[0]), int(right[1])+1)
    # print(range1, range2)
    return range1.start in range2 and range1[-1] in range2


def overlaps_at_all(left, right):
    range1 = range(int(left[0]), int(left[1])+1)
    range2 = range(int(right[0]), int(right[1])+1)
    # print(range1, range2)
    return range1.start in range2 or range1[-1] in range2


data = datareader("../day4.txt", translate=split_rows)


part1_score = 0
part2_score = 0
for left, right in data:
    print(
        f"line '{left}' '{right}' {contains_one_another(left, right)} {contains_one_another(right, left)}")
    if contains_one_another(left, right) or contains_one_another(right, left):
        part1_score += 1
    if overlaps_at_all(left, right) or overlaps_at_all(right, left):
        part2_score += 1

print(f"part1 score: {part1_score} part2 score: {part2_score}")


# part 2
