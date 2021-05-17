"""
Turtle logic

NOTE:
1.(Not Implemented)In Netlogo's implementation, agent initial age is set to randint(0, life_expectancy_max) ???
2.(Implemented)In Netlogo's implementation, agent initial wealth is set to metabolism + randint(0, 50)
"""
import random


class Agent:

    def __init__(self, life_expectancy_min, life_expectancy_max, max_metabolism, max_vision, x, y):
        """
        Initializes an agent with location, life_expectancy, metabolism & vision;
        Calls initialize() to finish setup
        """
        self.life_expectancy_min = life_expectancy_min
        self.life_expectancy_max = life_expectancy_max
        self.max_metabolism = max_metabolism
        self.max_vision = max_vision
        self.life_expectancy = None
        self.metabolism = None
        self.vision = None
        self.age = None
        self.x = None
        self.y = None
        self.wealth = None
        self.initialize(self, x, y)

    def initialize(self, x, y, offspring=False):
        """
        Sets initial status of an agent
        """
        self.life_expectancy = random.randint(self.life_expectancy_min, self.life_expectancy_max)
        self.metabolism = random.randint(1, self.max_metabolism)
        self.vision = random.randint(1, self.max_vision)
        self.age = 0
        self.x = x
        self.y = y
        if not offspring:
            self.wealth = self.metabolism + random.randint(0, 50)

    def aging(self):
        """Ages"""
        self.age += 1

    def harvest(self, world):
        """Harvests the land and add to possession"""
        self.wealth += world.get_grain(self.x, self.y)
        world.harvest_grain(self.x, self.y)

    def metabolize(self):
        """Metabolizes if still has grain"""
        self.wealth -= self.metabolism

    def is_dead(self):
        """Dies from starvation or aging"""
        return self.wealth <= 0 or self.age >= self.life_expectancy

    def reproduce(self, world):
        """
        Reproduces an offspring with same parameters except for wealth
        Wealth ranging from the poorest person’s amount of grain to the richest person’s amount of grain
        Calls initialize() to re-setup
        """
        if self.is_dead():
            self.initialize(self, self.x, self.y, offspring=True)
            self.wealth = random.randint(world.wealth_min, world.wealth_max)

    # TODO: moving logic


'''
    def move(self, world):
        """Core logic for navigating the world"""
        
'''
