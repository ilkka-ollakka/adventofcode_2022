#!/usr/bin/env python3
from textwrap import wrap


def datareader(filename, translate=int):
    with open(filename, "r") as fileinput:
        for dataline in fileinput:
            yield translate(dataline.strip())


def codeword_at_time(string_to_split):
    for codepiece in string_to_split:
        yield codepiece


def find_start_key(codeword, length_of_key):
    for line in codeword:
        stack = []
        for position, code in enumerate(list(line)):
            # print(code, position)
            stack.append(code)
            if len(stack) < length_of_key:
                continue
            if len(stack) > length_of_key:
                stack.pop(0)
            if len(set(stack)) == length_of_key:
                print(
                    f"found {length_of_key} unique position in {position +1} for string size {len(line)}")
                break
            # print(stack)


codeword = datareader("../day6.txt", translate=str)
find_start_key(codeword, 4)


codeword = datareader("../day6.txt", translate=str)
find_start_key(codeword, 14)

# print(piles)
# print(instructions)
