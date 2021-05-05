import random


def setup(settings):
    """Setup the world from parameters"""
    x = settings['x']
    y = settings['y']
    #growth_interval = settings['growth_interval']
    #percent_best_land = settings['percent_best_land']
    return [[{'grain': 0, 'agent': 0} for i in range(x)] for j in range(y)]

settings = {
    'x': 10,
    'y': 10
}
print(setup(settings))
