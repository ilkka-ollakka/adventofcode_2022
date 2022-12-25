#!/usr/bin/env python3

from collections import deque
from copy import deepcopy
from functools import lru_cache
from frozendict import frozendict


def datareader(filename: str, translator=str):
    with open(filename) as fileinput:
        for line in fileinput:
            yield translator(line)


def parse_blueprint(recipe: str) -> tuple[int, dict]:
    data = recipe.split()
    number = int(data[1][:-1])
    ore_cost = int(data[6])
    clay_cost = int(data[12])
    obsidian_ore = int(data[18])
    obsidian_clay = int(data[21])
    geode_ore = int(data[27])
    geode_obsidian = int(data[30])
    return number, {'ore': {'ore': ore_cost},
                    'clay': {'ore': clay_cost},
                    'obsidian': {'ore': obsidian_ore, 'clay': obsidian_clay},
                    'geode': {'ore': geode_ore, 'obsidian': geode_obsidian}}


def create_max_resources(recipes):
    max_resource_needs = {}
    for target in ['geode', 'obsidian', 'clay', 'ore']:
        amounts = recipes.get(target)
        for item in amounts:
            if item not in max_resource_needs:
                max_resource_needs[item] = amounts[item]
            else:
                max_resource_needs[item] = max(
                    [amounts[item], max_resource_needs[item]])
    return max_resource_needs


def check_possible_actions(resources, recipes, resource_intake, max_resource_needs, cache):
    actions = []
    # Check from best action to take
    # print(f"checking if {resources} is enought for {recipes}")
    cache_key = tuple([*resources.values(),
                       *resource_intake.values(),
                       *max_resource_needs.values()])

    if cache_key in cache:
        return cache[cache_key]

    for target in ['geode', 'obsidian', 'clay', 'ore']:
        amounts = recipes.get(target)
        all_enough = True

        if 0 and target == 'ore' and resource_intake[target] >= max_resource_needs[target]:
            # print(
            #     f"already enough robots for {target} {max_resource_needs} vs {resource_intake}")
            continue

        for item in amounts:
            # print(
            #     f"amounts of {item} for {target}-robot: needs: {amounts[item]} we have:{resources.get(item)}")
            if amounts[item] > resources.get(item):
                # print(
                #     f"not enough {item} for {target}-robot, checking if we can make {item}-robot")
                all_enough = False
        if all_enough is True:
            actions.append(target)

    # print(f"Adding none actions as following are left {actions}")

    actions.append(None)
    cache[cache_key] = actions
    return actions


def accumulate_resources(resources, resource_intake):
    result = deepcopy(resources)
    for item in result:
        result[item] += resource_intake[item]
    return result


def create_new_robot(resources, resource_intake, robot_type, recipes):
    needed_amounts = recipes.get(robot_type)
    new_resources = deepcopy(resources)
    for item in needed_amounts:
        new_resources[item] -= needed_amounts[item]
    new_resource_intake = deepcopy(resource_intake)
    new_resource_intake[robot_type] += 1
    return new_resources, new_resource_intake


@lru_cache
def triangle(time_left):
    return sum([i for i in range(0, time_left - 2)])


@lru_cache
def check_if_terminating(time_left, geode_incoming, geode_amounts, best_so_far):
    if (((time_left * geode_incoming) + geode_amounts + triangle(time_left)) <= best_so_far):
        return True
    return False


def find_geode_amounts(time_left, recipes, resource_intake, resources, max_resource_needs, cache, best_so_far=0, steps=set()):
    if time_left <= 0:
        score = resources['geode']
        if score > best_so_far:
            print(
                f"reached end with {resources} and intake of {resource_intake} steps {sorted(steps, key=lambda x: x[1], reverse=True)}")
        return resources['geode']

    cache_key = tuple([*resources.values(),
                      time_left, *resource_intake.values()])

    if cache_key in cache:
        return cache[cache_key]

    if check_if_terminating(time_left, resource_intake['geode'], resources['geode'], best_so_far):
        # print(
        #     f"no point searching further time left:{time_left} optimistic: {(time_left * resource_intake['geode']) + resources['geode']} vs {best_so_far}")
        return 0

    possible_actions = check_possible_actions(
        resources, recipes, resource_intake, max_resource_needs, cache)

    results = [best_so_far]
    for action in possible_actions:
        if action == None:
            new_resources = accumulate_resources(resources, resource_intake)

            results.append(find_geode_amounts(
                time_left - 1, recipes, resource_intake, new_resources, max_resource_needs, cache, max(results), steps | set([(None, time_left)])))

        elif action in ['obsidian', 'geode', 'clay', 'ore']:
            new_resources, new_resource_intake = create_new_robot(
                resources, resource_intake, action, recipes)

            new_resources = accumulate_resources(
                new_resources, resource_intake)

            results.append(find_geode_amounts(
                time_left -
                1, recipes, new_resource_intake, new_resources, max_resource_needs, cache, max(
                    results), steps | set([(action, time_left)])
            ))
        else:
            print(f"Odd action received!! {action}")

    cache[cache_key] = max(results)
    return max(results)


initial_resource_intake = {'ore': 1, 'clay': 0,
                           'obsidian': 0, 'geode': 0}
initial_minutes_left = 24

recipes = {}

for recipe_number, recipe in datareader("../day19.txt", parse_blueprint):
    print(recipe_number, recipe)
    recipes[recipe_number] = recipe

results = {}
part2_results = {}
for recipe in recipes:

    # results[recipe] = find_geode_amounts(initial_minutes_left, recipes[recipe], initial_resource_intake, {
    #                                      'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0}, max_resources, {})
    # print(f"new results added {results}")

    def sim(ore_cost, clay_cost, obsidian_cost, geode_cost, time):
        q = deque([(0, 1, 0, 0, 0, 0, 0, 0, time)])
        visited = set()

        best = 0
        max_ore_amount = max(ore_cost, clay_cost,
                             obsidian_cost[0], geode_cost[0])

        while q:
            ore, incoming_ore, clay, incoming_clay, obsidian, incoming_obsidian, geode, incoming_geode, time = x = q.pop()

            if x in visited:
                continue

            visited.add(x)

            incoming_ore = min(incoming_ore, max_ore_amount)

            new_ore = ore + incoming_ore
            new_clay = clay + incoming_clay
            new_obs = obsidian + incoming_obsidian
            new_geo = geode + incoming_geode
            time -= 1

            if time == 0:
                best = max(best, new_geo)
                continue

            # check early termination
            #check_if_terminating(time_left, geode_incoming, geode_amounts, obsidian_incoming, obsidian_needs, best_so_far)
            if 0 and check_if_terminating(time, incoming_geode, new_geo, incoming_obsidian, new_obs, best):
                continue

            added_something_to_queue = False
            # Build geode if possible
            if ore >= geode_cost[0] and obsidian >= geode_cost[1]:
                new_ore2 = new_ore - geode_cost[0]
                new_obs2 = new_obs - geode_cost[1]
                new_incoming_geode = incoming_geode + 1
                q.append((new_ore2, incoming_ore, new_clay, incoming_clay,
                         new_obs2, incoming_obsidian, new_geo, new_incoming_geode, time))
                added_something_to_queue = True
                continue

            # build obsidian if geode not possible
            if ore >= obsidian_cost[0] and clay >= obsidian_cost[1]:
                new_ore2 = new_ore - obsidian_cost[0]
                new_clay2 = new_clay - obsidian_cost[1]
                new_incoming_obsidian = incoming_obsidian + 1
                q.append((new_ore2, incoming_ore, new_clay2, incoming_clay,
                         new_obs, new_incoming_obsidian, new_geo, incoming_geode, time))
                added_something_to_queue = True

            # if obsidian not working, check clay
            if ore >= clay_cost:
                new_ore2 = new_ore - clay_cost
                new_incoming_clay = incoming_clay + 1
                q.append((new_ore2, incoming_ore, new_clay, new_incoming_clay,
                         new_obs, incoming_obsidian, new_geo, incoming_geode, time))
                added_something_to_queue = True

            if ore >= ore_cost:
                new_ore2 = new_ore - ore_cost
                new_incoming_ore = incoming_ore + 1
                q.append((new_ore2, new_incoming_ore, new_clay, incoming_clay,
                         new_obs, incoming_obsidian, new_geo, incoming_geode, time))
                added_something_to_queue = True

            #
            q.append((new_ore, incoming_ore, new_clay, incoming_clay,
                      new_obs, incoming_obsidian, new_geo, incoming_geode, time))

        print(f'best currently {best} visited {len(visited)}')
        return best

    max_resources = create_max_resources(recipes[recipe])
    results[recipe] = find_geode_amounts(initial_minutes_left, recipes[recipe], initial_resource_intake, {
                                         'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0}, max_resources, {})
    if len(part2_results) < 3:
        part2_results[recipe] = find_geode_amounts(32, recipes[recipe], initial_resource_intake, {
            'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0}, max_resources, {})
    # def sim(ore_cost, clay_cost, obsidian_cost, geode_cost, time):
    """ current_recipe = recipes[recipe]
    results[recipe] = sim(current_recipe['ore']['ore'], current_recipe['clay']['ore'],
                          [current_recipe['obsidian']['ore'],
                              current_recipe['obsidian']['clay']],
                          [current_recipe['geode']['ore'],
                              current_recipe['geode']['obsidian']],
                          24)
    if len(part2_results) < 3:
        part2_results[recipe] = sim(current_recipe['ore']['ore'], current_recipe['clay']['ore'],
                                    [current_recipe['obsidian']['ore'],
                                     current_recipe['obsidian']['clay']],
                                    [current_recipe['geode']['ore'],
                                     current_recipe['geode']['obsidian']],
                                    32) """
    print(f"new results added {results} {part2_results}")


print(results)
quality_level = 0
for result in results:
    quality_level += (result * results[result])
print(f"part1: {quality_level}")

# part 2
result_product = 1
for result in part2_results.values():
    result_product *= result
print(f"part2: {result_product}")
