"""

"""
import random
import time
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


def go(agents, world, result, report_tick=1, tick_time=1):
    """Run simulation, with tick length in time and report per tick"""
    for agent in agents:
        agent.move(world)
    for agent in agents:
        agent.harvest(world)
    for agent in agents:
        agent.metabolize()
    for agent in agents:
        agent.aging()
    for agent in agents:
        agent.reproduce(world)
    result.load_result(report_tick, world, agents)
    result.stepwise_report()
    world.refresh()
    time.sleep(tick_time)
# def display(world):

# if __name__ == '__main__':
#    spawn_agent()
