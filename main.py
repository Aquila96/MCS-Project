"""
Wealth Distribution simulation entrypoint
"""
import json

from agent import Agent
from plot import average, plot_gini_multiple
from world import World
from result import Result
import utils


def setup():
    # Construct world
    result = Result()
    world = World(settings['x'],
                  settings['y'],
                  settings['max_grain'],
                  settings['percent_best_land'],
                  settings['grain_growth_interval'],
                  settings['num_grain_grown'])

    # Set common variables
    Agent.patch_purchase_buffer = settings['agent_purchase_patch_buffer']
    World.rent_percentage = settings['rent_percentage_of_yield']
    World.patch_price_multiplier = settings['purchase_price_multiplier']

    # Spawn all agents
    agents = []
    for _ in range(settings['num_people']):
        agents.append(utils.spawn_agent(settings, world))

    return result, world, agents


def run_indefinitely():
    result, world, agents = setup()
    iteration = 0
    while 1:
        utils.go(iteration, agents, world, result,
                 settings['reproducing_error'] == 1,
                 settings['property_extension'] == 1,
                 settings['inherit_extension'] == 1,
                 report_interval=settings['report_interval'],
                 refresh_interval=settings['refresh_interval'])
        iteration += 1


def run_limit(n_iterations):
    result, world, agents = setup()
    iteration = 0
    while iteration < n_iterations:
        utils.go(iteration, agents, world, result,
                 settings['reproducing_error'] == 1,
                 settings['property_extension'] == 1,
                 settings['inherit_extension'] == 1,
                 report_interval=settings['report_interval'],
                 refresh_interval=settings['refresh_interval'])
        iteration += 1

    return result


def run_multiple(n_iterations, n_times):
    results = []
    for i in range(n_times):
        results += [run_limit(n_iterations)]
    cum_avg = 0
    for result in results:
        cum_avg += average(result.gini_index)

    print("Average Gini: " + str(cum_avg / len(results)))
    plot_gini_multiple(n_iterations, results)


# TODO: Beautify output
if __name__ == '__main__':

    # Import Settings
    with open('settings.json') as f:
        settings = json.load(f)
        f.close()

    # Run and display
    run_multiple(1000, 5)
