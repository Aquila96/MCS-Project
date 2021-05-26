"""
Wealth Distribution simulation entrypoint
"""
import json
from world import World
from result import Result
import utils

# TODO: Beautify output
if __name__ == '__main__':
    with open('settings.json') as f:
        settings = json.load(f)
        f.close()
    # Construct world
    result = Result()
    world = World(settings['x'],
                  settings['y'],
                  settings['max_grain'],
                  settings['percent_best_land'],
                  settings['grain_growth_interval'],
                  settings['num_grain_grown'])
    # Spawn all agents
    agents = []
    for _ in range(settings['num_people']):
        agents.append(utils.spawn_agent(settings, world))
    # Run and display
    iteration = 0
    while 1:
        utils.go(iteration, agents, world, result,
                 settings['reproducing_error'] == 1,
                 settings['education_extension'] == 1,
                 settings['education_cost_factor'],
                 settings['education_vision_increase'],
                 report_interval=settings['report_interval'],
                 refresh_interval=settings['refresh_interval'])
        iteration += 1
