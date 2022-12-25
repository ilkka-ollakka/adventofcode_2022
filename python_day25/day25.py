#!/usr/bin/env python3.10

import math


def datareader(filename, translator=str):
    with open(filename) as file_input:
        for line in file_input:
            yield translator(line)


def parse_5_base(input_string: str) -> int:
    mapping = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
    symbols = list(input_string.strip())
    symbols.reverse()
    result = 0
    for position, symbol in enumerate(symbols):
        power = 5 ** position
        result += (power * mapping[symbol])

    return result


def convert_to_5_base(input_number: int) -> str:
    output = []
    # calculate highest power we need
    while input_number != 0:
        current_digit = (input_number + 2) % 5 - 2
        digit = None
        match current_digit:
            case -2:
                digit = '='
            case -1:
                digit = '-'
            case 0:
                digit = '0'
            case 1:
                digit = '1'
            case 2:
                digit = '2'
        output.append(digit)
        input_number = int((input_number + 2) / 5)
        print(input_number)
    output.reverse()
    return "".join(output)


result = 0
for number in datareader("../day25.txt", parse_5_base):
    result += number
print(result)
print(convert_to_5_base(result))
