import random
from agent import Agent


def spawn_agent(settings, world):
    """Spawns an agent at a free location"""
    life_expectancy_min = settings['life_expectancy_min']
    life_expectancy_max = settings['life_expectancy_max']
    max_metabolism = settings['max_metabolism']
    max_vision = settings['max_vision']
    # TODO: random choice free locations
    x, y = random.choice()
    agent = Agent(life_expectancy_min,
                  life_expectancy_max,
                  max_metabolism,
                  max_vision,
                  x,
                  y)
    world.set_agent(x, y, agent)

# if __name__ == '__main__':
#    spawn_agent()
