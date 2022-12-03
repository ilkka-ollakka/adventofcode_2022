#!/usr/bin/env python3

def datareader(filename, translate=int):
    with open(filename, "r") as fileinput:
        for dataline in fileinput:
            yield translate(dataline.strip())


def split_rows(row):
    row_length = int(len(row)/2)
    (left, right) = set(list(row[:row_length])), set(list(row[row_length:]))

    # print(left, right)

    return left, right


data = datareader("../day3.txt", translate=split_rows)

priorities = [chr(x) for x in range(ord('a'), ord('z')+1)]
priorities.extend([chr(x) for x in range(ord('A'), ord('Z')+1)])


score = 0
for left, right in data:
    print(f"line '{left}' '{right}' common: {left & right}")
    common_item = list(left & right)[0]
    # print(f"common item: {common_item}")
    score += (priorities.index(common_item) + 1)
    print(f" score: {priorities.index(common_item)}")

print(score)


# part 2

data = datareader("../day3.txt", translate=split_rows)
score = 0
stack = []
for left, right in data:
    print(f"line '{left}' '{right}' common: {left & right}")
    common_item = (left | right)
    if len(stack) == 2:
        print(f"checking common item on 3 sacks: {common_item}")
        common_item &= stack.pop()
        print(f"first 2 common left {common_item}")
        common_item &= stack.pop()
        print(f"common item left {common_item}")
        common_item = list(common_item)[0]
        score += (priorities.index(common_item) + 1)
        continue
    stack.append(common_item)

    # print(f"common item: {common_item}")
    # score += (priorities.index(common_item) + 1)
    # print(f" score: {priorities.index(common_item)}")
print(score)
