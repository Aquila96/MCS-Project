import json
from world import World
from utils import spawn_agent

if __name__ == '__main__':
    with open('settings.json') as f:
        settings = json.load(f)
        f.close()

    world = World(settings['x'],
                  settings['y'],
                  settings['max_grain'],
                  settings['percent_best_land'],
                  settings['grain_growth_interval'],
                  settings['num_grain_grown'])
    print(world.patches)
    # TODO: random choice free locations
    #for i in range(settings['num_people']):
    #    spawn_agent(settings, world)
