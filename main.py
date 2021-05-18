"""
Wealth Distribution simulation entrypoint
"""
import json
import time
from world import World
from utils import spawn_agent

# TODO: Beautify output
if __name__ == '__main__':
    with open('settings.json') as f:
        settings = json.load(f)
        f.close()
    # Construct world
    world = World(settings['x'],
                  settings['y'],
                  settings['max_grain'],
                  settings['percent_best_land'],
                  settings['grain_growth_interval'],
                  settings['num_grain_grown'])
    # Spawn all agents
    agents = []
    for _ in range(settings['num_people']):
        agents.append(spawn_agent(settings, world))
    # Run and display
    while 1:
        for agent in agents:
            agent.go(world)
        world.refresh()
        # display(world)
        time.sleep(1)
