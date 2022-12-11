#!/usr/bin/env python3

from math import lcm


def datareader(filename: str, translate=str) -> list[str]:
    with open(filename, "r") as fileinput:
        for dataline in fileinput:
            yield translate(dataline.strip())


class Monkey(object):

    def __init__(self):
        self.items = []
        self.number = 0
        self.modulator = 1
        self.operation = None
        self.items_inspected = 0
        self.test_operation = {"dividor": 2,
                               "false_path": None, "true_path": None}

    # test items and returns list of (target, item)
    def test_items(self) -> list[tuple[int, int]]:
        results = []
        while self.items:
            item = self.items.pop(0)
            self.items_inspected += 1
            item_output = int(self.evaluate(item))
            # for part 1 change this to int(int(item_output) / 3)
            item_test_value = int(int(int(item_output)) % self.modulator)
            if item_test_value % self.test_operation["dividor"] == 0:
                results.append(
                    (self.test_operation["true_path"], item_test_value))
            else:
                results.append(
                    (self.test_operation["false_path"], item_test_value))
        return results

    def evaluate(self, input_value):
        # print(f"operations {self.operation} with value {input_value}")
        if self.operation[1] == "*":
            output = 1
            for value in [self.operation[0], self.operation[2]]:
                if value == "old":
                    value = int(input_value)
                output *= int(value)
            result = output
        else:
            output = 0
            for value in [self.operation[0], self.operation[2]]:
                if value == "old":
                    value = int(input_value)
                output += int(value)
            result = output
        # print(f"Outcome value {result}")
        return result

    def __str__(self):
        return f"monkey {self.number} score: {self.items_inspected} items: {self.items} test: {self.test_operation} operator: {self.operation}"


def parse_monkeys(string: str) -> Monkey:
    monkey = Monkey()

    # print(f"monkey-data: '{string}'")

    for line in string.split('\n'):
        if line.startswith("Monkey "):
            number = line.split(' ')[1]
            monkey.number = int(number.split(':')[0])
            continue
        if line.startswith("Starting items:"):
            items = line.split(':')[1]
            monkey.items = [int(x) for x in items.split(', ')]
            continue
        if line.startswith("Operation:"):
            operation = line.split("=")[1]
            monkey.operation = operation.strip().split()
            continue
        if line.startswith("Test: "):
            divisor = int(line.split("by")[1])
            monkey.test_operation["dividor"] = divisor
            continue
        if line.startswith("If true"):
            true_target = int(line.split(' ')[-1])
            monkey.test_operation["true_path"] = true_target
            continue
        if line.startswith("If false"):
            false_target = int(line.split(' ')[-1])
            monkey.test_operation["false_path"] = false_target
            continue

    return monkey


if __name__ == "__main__":
    data_input = "\n".join(datareader(
        "../day11.txt", str)).split("\n\n")

    monkeys = {}

    for monkey_string in data_input:
        monkey = parse_monkeys(monkey_string)
        monkeys[monkey.number] = monkey

    dividors = []
    # collect dividors
    for monkey in monkeys.values():
        dividors.append(int(monkey.test_operation["dividor"]))

    dividor = lcm(*dividors)

    for monkey in monkeys.values():
        monkey.modulator = dividor

    for i in range(0, 10000):
        for monkey_number in sorted(monkeys.keys()):
            # print(monkey_number)
            results = monkeys[monkey_number].test_items()
            for target, value in results:
                monkey = monkeys[target]
                monkey.items.append(value)

    scores = [monkey.items_inspected for monkey in monkeys.values()]
    scores.sort()
    print(f"items inspected {scores}")
    print(f"result score: {scores.pop() * scores.pop()}")
    print(f"lcm {dividor}")
