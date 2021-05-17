"""

"""
import random
from agent import Agent


# TODO: Beautify output
def spawn_agent(settings, world):
    """Spawns an agent at a free location"""
    x, y = random.choice(world.list_empty_patch())
    agent = Agent(settings['life_expectancy_min'],
                  settings['life_expectancy_max'],
                  settings['max_metabolism'],
                  settings['max_vision'],
                  x, y)
    world.set_agent(x, y, agent)
    return agent

# def display(world):

# if __name__ == '__main__':
#    spawn_agent()
