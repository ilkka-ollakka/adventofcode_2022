#!/usr/bin/env python3

shape_score = {'A': 1, 'B': 2, 'C': 3}
outcome_score = {'Y': 3, 'Z': 6, 'X': 0}
win_conditions = {'A': 'B', 'B': 'C', 'C': 'A'}
draw_conditions = {'A': 'A', 'B': 'B', 'C': 'C'}
lose_conditions = {'A': 'C', 'B': 'A', 'C': 'B'}
outcome_mapping = {'Z': win_conditions,
                   'Y': draw_conditions,
                   'X': lose_conditions}


def datareader(filename, translate=int):
    with open(filename, "r") as fileinput:
        for dataline in fileinput:
            yield translate(dataline.strip())


def split_rows(row):
    return row.split(' ')


def outcome(opponent, own):
    return outcome_score.get(own)


def get_shape_score(opponent, own_outcome):
    own_mapping = outcome_mapping.get(own_outcome)
    own = own_mapping.get(opponent)
    print(f'shape score for {own} is {shape_score.get(own)}')
    return shape_score.get(own)


data = datareader("../day2.txt", translate=split_rows)

score = 0
for opponent, end_result in data:
    # print(f"line {linenumber} data: '{line}'")
    print(f"Opponent chose {opponent} I chose {end_result}")
    score += outcome(opponent, end_result)
    score += get_shape_score(opponent, end_result)

print(score)
