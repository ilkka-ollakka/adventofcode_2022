#!/usr/bin/env python3

from functools import lru_cache
from itertools import combinations, permutations


def datareader(filename, translator):
    with open(filename) as inputfile:
        for line in inputfile:
            yield translator(line)


def parse_valves(input_line):
    lines = input_line.split()
    name = lines[1]
    flow_rate = int(lines[4].split("=")[1][:-1])
    connections = "".join(lines[9:]).split(",")
    return name, flow_rate, connections


valve_network = {}
for name, flow_rate, connections in datareader('../day16.txt', parse_valves):
    # print(name, flow_rate, connections)
    valve_network[name] = {'flow': flow_rate, 'connections': connections}

for valve in valve_network:
    print(valve, valve_network.get(valve))

current_position = 'AA'
time_left = 30
opened_valves = set()
max_flow = 0

potential_valves = set([
    valve for valve in valve_network if valve_network[valve]["flow"] > 0])


def find_route(current_point, target, steps=0, visited_points=set()):
    if current_point == target:
        return steps
    point = valve_network.get(current_point)
    if target in point['connections']:
        return steps + 1
    routes = []
    for next_point in point['connections']:
        if next_point in visited_points:
            continue
        route_speed = find_route(
            next_point, target, steps + 1, visited_points | set([current_point]))
        if route_speed is not None:
            routes.append(route_speed)
    if routes:
        return min(routes)


def calculate_flow(opened_valves, valve_network):
    # print("calculating final score")
    score = 0
    for valve, time_point in opened_valves:
        # print(f"opened valve {valve} in time {time_point}")
        score += (max([0, time_point]) * valve_network.get(valve)["flow"])
    # print(
    #     f"calculating final score as {score} for {sorted(opened_valves, key=lambda x: x[1], reverse=True)}")
    return score


def find_max_flow(current_point, time_left, opened_valves, valve_network, potential_valves, route_speeds):
    if time_left <= 0 or len(potential_valves) == 0:
        return calculate_flow(opened_valves, valve_network), opened_valves
    current = valve_network.get(current_point)
    max_flows = []
    for valve in potential_valves:
        # print(f"{current_point} to {valve} with values {valve_network.get(valve)}")
        steps_to_take = route_speeds[current_point][valve]
        new_time = time_left - steps_to_take - 1
        if new_time <= 0:
            print(
                f"route {current_point} to {valve} took too much {time_left} -> {new_time}")
            max_flows.append(
                (calculate_flow(opened_valves, valve_network), opened_valves))
            continue
        flow_result = find_max_flow(valve, new_time, opened_valves | set(
            [(valve, new_time)]), valve_network, potential_valves - set([valve]),
            route_speeds)
        if flow_result:
            flow, flow_route = flow_result
            max_flows.append((flow, flow_route))
    if max_flows:
        return max(max_flows)


# prepopulate distances/routes between potential valves
route_speeds = {}

for source_valve in potential_valves | set(["AA"]):
    for target_valve in potential_valves:
        distance = find_route(source_valve, target_valve)
        if source_valve not in route_speeds:
            route_speeds[source_valve] = {target_valve: distance}
        else:
            route_speeds[source_valve][target_valve] = distance

# result = find_max_flow(current_position, time_left,
#                        opened_valves, valve_network, potential_valves, route_speeds)
# if result:
#     score, route = result
#    print(f"max score found {score}")
#    print(f"with route {sorted(route, key=lambda x: x[1], reverse=True)}")
# print(result)


# part 2

def find_max_flow_multiposition(current_points, times_left, opened_valves, valve_network, potential_valves, route_speeds):
    if len(potential_valves) == 0:
        return calculate_flow(opened_valves, valve_network), opened_valves
    my_current = valve_network.get(current_points[0])
    elephan_current = valve_network.get(current_points[1])
    max_flows = []
    for valves in combinations(potential_valves, 2):
        # print(f"{current_point} to {valve} with values {valve_network.get(valve)}")
        my_valve = valves[0]
        my_position, elephant_position = current_points
        elephant_valve = valves[1]
        # print(my_valve, elephant_valve)
        steps_to_take_for_me = route_speeds[my_position][my_valve]
        steps_to_take_for_elephant = route_speeds[elephant_position
                                                  ][elephant_valve]
        new_time_for_me = times_left[0] - steps_to_take_for_me - 1
        new_time_for_elephant = times_left[1] - steps_to_take_for_elephant - 1

        flow_result = find_max_flow_multiposition(valves, [new_time_for_me, new_time_for_elephant], opened_valves | set(
            [(my_valve, new_time_for_me), (elephant_valve, new_time_for_elephant)]), valve_network, potential_valves - set(valves),
            route_speeds)
        if flow_result:
            flow, flow_route = flow_result
            max_flows.append((flow, flow_route))
    if max_flows:
        print(max(max_flows))
        return max(max_flows)


result = find_max_flow_multiposition(["AA", "AA"], [26, 26],
                                     set(), valve_network, potential_valves, route_speeds)
if result:
    score, route = result
    print(f"max score found {score}")
    print(f"with route {sorted(route, key=lambda x: x[1], reverse=True)}")
print(result)
