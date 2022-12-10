#!/usr/bin/env python3

def datareader(filename: str, translate=str) -> list[str]:
    with open(filename, "r") as fileinput:
        for dataline in fileinput:
            yield translate(dataline.strip())


def parse_commands(string) -> tuple[int, int]:
    commands = string.split()
    if commands[0] == 'noop':
        return (1, 0)
    else:
        return (2, int(commands[1]))


if __name__ == "__main__":
    data_input = datareader("../day10.txt", parse_commands)

    cycle_number = 0
    register_value = 1
    drawing_position = (0, 0)

    cycle_milestones = [x for x in range(40, 241, 40)]
    cycle_values = []
    crt_screen = [[" " for x in range(0, 41)] for x in range(0, 7)]

    cycle, increment = next(data_input)

    for cycle_number in range(0, 241):

        if cycle_number >= cycle_milestones[0]:
            print(
                f"Cycle milestone reached {cycle_number} register {register_value}")
            cycle_values.append(cycle_milestones[0] * register_value)
            cycle_milestones.pop(0)
            drawing_position = (drawing_position[0] + 1, 0)
            if len(cycle_milestones) == 0:
                break

        if (drawing_position[1] - 1) <= register_value <= (drawing_position[1] + 1):
            print(
                f"Would hit drawing position {drawing_position} {register_value}")
            crt_screen[drawing_position[0]][drawing_position[1]] = "#"
        else:
            crt_screen[drawing_position[0]][drawing_position[1]] = "."

        cycle -= 1
        if cycle == 0:
            register_value += increment
            try:
                cycle, increment = next(data_input)
            except StopIteration:
                break

        drawing_position = (
            drawing_position[0], drawing_position[1] + 1)

    print(cycle_values)
    print(sum(cycle_values))
    print("\n".join(["".join(x) for x in crt_screen]))
