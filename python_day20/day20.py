#!/usr/bin/env python3.10

from collections import deque


def datareader(filename, translator=str):
    with open(filename, 'r') as fileinput:
        for line in fileinput:
            yield translator(line)


def part1():
    coordinates = deque([])
    codeword = deque([])
    for position, number in enumerate(datareader("../day20.txt", int)):
        coordinates.append((number, position))
        codeword.append((position, number))

    # print(coordinates, len(coordinates))
    length_of_coordinates = len(coordinates) - 1
    print(f"amount of codewords {len(codeword)}")

    for number, position in coordinates:
        new_position = old_position = codeword.index((position, number))
        if codeword.count((position, number)) != 1:
            print(
                f"number {number} is stored {codeword.count((position, number))} times!")
        codeword.rotate(-new_position)
        # print(number, codeword[0])
        number_to_move = codeword.popleft()

        rotate_amount = number % length_of_coordinates
        codeword.rotate(-rotate_amount)
        codeword.insert(0, number_to_move)
        # print(f"moving number {number_to_move} from {old_position} to {position}")
        # print(f"current state {codeword}")

    # print(codeword)
    codepoints = [1000, 2000, 3000]
    print(f"Checking numbers from {codepoints} positions")
    codenumbers = []

    while True:
        _, number = codeword[0]
        if number == 0:
            break
        codeword.rotate(1)

    for codepoint in codepoints:
        codeword.rotate(-1000)
        codenumbers.append(codeword[0][1])
    print(f"numbers {codenumbers} result {sum(codenumbers)}")


def part2():
    coordinates = deque([])
    codeword = deque([])
    decryption_key = 811589153
    for position, number in enumerate(datareader("../day20.txt", int)):
        coordinates.append((number * decryption_key, position))
        codeword.append((position, number * decryption_key))

    # print(coordinates, len(coordinates))
    length_of_coordinates = len(coordinates)-1
    print(f"amount of codewords {len(codeword)}")

    for _ in range(0, 10):
        for number, position in coordinates:
            new_position = old_position = codeword.index((position, number))
            if codeword.count((position, number)) != 1:
                print(
                    f"number {number, position} is stored {codeword.count((position, number))} times!")
            codeword.rotate(-new_position)
            # print(number, codeword[0])
            number_to_move = codeword.popleft()

            rotate_amount = number % length_of_coordinates

            codeword.rotate(-rotate_amount)
            codeword.insert(0, number_to_move)
            # print(f"moving number {number_to_move} from {old_position} to {position}")
            # print(f"current state {codeword}")

    # print(codeword)
    codepoints = [1000, 2000, 3000]
    print(f"Checking numbers from {codepoints} positions")
    codenumbers = []

    while True:
        _, number = codeword[0]
        if number == 0:
            break
        codeword.rotate(1)

    for codepoint in codepoints:
        codeword.rotate(-1000)
        codenumbers.append(codeword[0][1])
    print(f"numbers {codenumbers} result part 2 {sum(codenumbers)}")


part1()
part2()

# print(f"codeword {codeword}")
