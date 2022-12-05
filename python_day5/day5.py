#!/usr/bin/env python3
from textwrap import wrap


def datareader(filename, translate=int):
    with open(filename, "r") as fileinput:
        for dataline in fileinput:
            yield translate(dataline.rstrip())


piles, instructions = "\n".join(
    list(datareader("../day5_example.txt", translate=str))).split('\n\n')


def parse_stack(piles):
    stacks = {}

    for line in piles.split('\n'):
        line_data = [line[i:i+4] for i in range(0, len(line), 4)]
        for stack_number, content in enumerate(line_data):
            stack_number += 1
            if stack_number not in stacks:
                stacks[stack_number] = []
            if content[1].isalpha():
                stacks[stack_number].append(content[1])
    return stacks


def part1(piles, instructions):

    stacks = parse_stack(piles)

    for command in instructions.split('\n'):
        code_split = command.split(' ')
        amount = int(code_split[1])
        source_stack = int(code_split[3])
        destination_stack = int(code_split[5])
        for moving in range(0, amount):
            stacks[destination_stack].insert(0,
                                             stacks[source_stack].pop(0)
                                             )
        # print(f"moving {amount} from {source_stack} to {destination_stack}")
        # print(stacks)

    final_state = []
    for stack in stacks.values():
        final_state.append(str(stack[0]))
    print(f"part1 code: {''.join(final_state)}")


def part2(piles, instructions):
    stacks = parse_stack(piles)

    for command in instructions.split('\n'):
        code_split = command.split(' ')
        amount = int(code_split[1])
        source_stack = int(code_split[3])
        destination_stack = int(code_split[5])
        moving_items = stacks[source_stack][:amount]
        for moving in range(0, amount):
            stacks[destination_stack].insert(0,
                                             moving_items.pop()
                                             )
        del stacks[source_stack][:amount]
        # print(f"moving {amount} from {source_stack} to {destination_stack}")
        # print(stacks)

    final_state = []
    for stack in stacks.values():
        final_state.append(str(stack[0]))
    print(f'part2 code: {"".join(final_state)}')


part1(piles, instructions)
part2(piles, instructions)
# print(piles)
# print(instructions)
