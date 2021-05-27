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


def go(iteration, agents, world, result, reproducing_error, education_extension, education_cost_percentage, education_vision_increase, inherit_extension, report_interval=1, refresh_interval=1):
    """Run simulation, with tick length in time and report per tick"""
    if education_extension and iteration > 0:
        education_cost = int(education_cost_percentage * (world.wealth_max + world.wealth_min) / 2)
        for agent in agents:
            agent.educate(education_vision_increase, education_cost)
    for agent in agents:
        agent.move(world)
    world.harvest()
    for agent in agents:
        #agent.harvest(world)
        agent.metabolize()
        agent.aging()
        agent.buy_land(world)
    for agent in agents:
        agent.reproduce(world, reproducing_error, inherit_extension)
    result.load_result(report_interval, world, agents)
    result.stepwise_report()
    world.refresh(iteration)
    time.sleep(refresh_interval)
# def display(world):

# if __name__ == '__main__':
#    spawn_agent()
