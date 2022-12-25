#!/usr/bin/env python3.10

from enum import Enum
from itertools import pairwise
from lib2to3.pgen2.token import PLUS


def datareader(filename, translator=str):
    with open(filename, 'r') as fileinput:
        for line in fileinput:
            yield translator(line)


def sum(left, right):
    return left + right


def minus(left, right):
    return left - right


def divided(left, right):
    return left // right


def product(left, right):
    return int(left * right)


def equal(left, right):
    return left == right


def set_any(left, right):
    if left is not None:
        return left
    return right


def opposite_operator(operator):
    if operator == sum:
        return minus
    if operator == minus:
        return sum
    if operator == product:
        return divided
    if operator == divided:
        return product
    if operator == equal:
        return set_any


def parse_monkey(input_line):
    data = input_line.split()
    identifier = data[0][:-1]
    evaluated_value = None
    left = None
    right = None
    operation = None
    if len(data[1:]) == 1:
        evaluated_value = int(data[1])
    else:
        left, operation_mark, right = data[1:]
        match operation_mark:
            case '-':
                operation = minus
            case '+':
                operation = sum
            case '*':
                operation = product
            case '/':
                operation = divided
            case _:
                print(f"Unknown operation found! '{operation_mark}'")
    return {'id': identifier, 'value': evaluated_value, 'left': left, 'right': right, 'operator': operation}


def evaluate_value(monkey, monkeys):
    if monkey['value']:
        return int(monkey['value'])
    left_side = monkeys[monkey['left']]
    right_side = monkeys[monkey['right']]
    operation = monkey['operator']
    # print(f"operation: {operation}")
    result = operation(evaluate_value(left_side, monkeys),
                       evaluate_value(right_side, monkeys))
    # monkey['value'] = result
    # print(f"monkey {monkey} evaluated to {result}")
    return int(result)


def find_route(monkeys, current_point, target, path=[]):
    if current_point == target:
        return path + [current_point]
    current_point = monkeys[current_point]
    for next in [current_point['left'], current_point['right']]:
        if next is None:
            continue
        route = find_route(monkeys, next, target, path + [current_point['id']])
        if route:
            return route


monkeys = dict()

for monkey_info in datareader("../day21.txt", parse_monkey):
    print(monkey_info)
    monkeys[monkey_info['id']] = monkey_info


print(
    f"value of root for part1: {int(evaluate_value(monkeys['root'], monkeys))}")


# Part 2
monkeys["root"]["operator"] = equal

route_between = find_route(monkeys, 'root', 'humn')


print("Evaluating opposite actions")
operations = []
stack = None
for current, next in pairwise(route_between):
    if current == 'root':
        # check if we need to match left or right:
        if next == monkeys[current]['left']:
            stack = evaluate_value(monkeys[monkeys[current]['right']], monkeys)
        else:
            stack = evaluate_value(monkeys[monkeys[current]['left']], monkeys)
        print(f"result of {next} needs to be {stack}")
        continue
    monkey = monkeys[current]
    operator = opposite_operator(monkey['operator'])
    current_stack = stack
    if monkey['left'] == next:
        value = evaluate_value(
            monkeys[monkey['right']], monkeys)
    else:
        value = evaluate_value(
            monkeys[monkey['left']], monkeys)
        if monkey['operator'] == minus:
            operator = minus
            stack = operator(value, stack)
            continue
    stack = operator(stack, value)
    print(f"{current} -> {next} {current_stack} {operator} {value} = {stack}")

print(stack)

monkeys['humn']['value'] = int(stack)
print(
    f"value of root for part2: {bool(evaluate_value(monkeys['root'], monkeys))} with humn value {monkeys['humn']['value']}")
print(f"route between is {route_between}")

print("root left and right:")
left = monkeys['root']['left']
right = monkeys['root']['right']
print(f"left: {evaluate_value(monkeys[left], monkeys)}")
print(f"right: {evaluate_value(monkeys[right], monkeys)}")

for monkey in route_between:
    print(monkeys[monkey])
    # print(evaluate_value(monkeys[monkey], monkeys))
