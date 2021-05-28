"""
Utilities helping the model to run 
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


def go(iteration,
       agents,
       world,
       result,
       reproducing_error,
       property_extension,
       inherit_extension,
       report_interval=1,
       refresh_interval=1):
    """Run simulation, with tick length in time and tick per report"""
    for agent in agents:
        agent.move(world)
    world.harvest()
    for agent in agents:
        agent.metabolize()
        agent.aging()
        if property_extension:
            agent.buy_land(world)
    for agent in agents:
        agent.reproduce(world, reproducing_error, inherit_extension)
    result.load_result(report_interval, world, agents)
    result.stepwise_report()
    world.refresh(iteration)
    time.sleep(refresh_interval)
