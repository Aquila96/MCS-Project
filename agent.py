import random

'''
NOTE: 
1.In Netlogo's implementation, agent initial age is set to randint(0, life_expectancy_max)
2.In Netlogo's implementation, agent initial wealth is set to metabolism + randint(0, 50)
'''


class Agent:

    def __init__(self, life_expectancy_min, life_expectancy_max, max_metabolism, max_vision, wealth, x, y):
        """
        Initializes an agent with location, life_expectancy, metabolism & vision;
        """
        self.life_expectancy = None
        self.metabolism = None
        self.vision = None
        self.age = None
        self.x = None
        self.y = None
        self.reset(self, life_expectancy_min, life_expectancy_max, max_metabolism, max_vision, x, y)
        self.wealth = wealth

    def reset(self, life_expectancy_min, life_expectancy_max, max_metabolism, max_vision, x, y):
        """
        Sets initial status of an agent
        """
        self.life_expectancy = random.randint(life_expectancy_min, life_expectancy_max)
        self.metabolism = random.randint(1, max_metabolism)
        self.vision = random.randint(1, max_vision)
        self.age = 0
        self.x = x
        self.y = y

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
        return self.wealth <= 0 or self.age == self.life_expectancy

    def reproduce(self, world):
        """
        Reproduces an offspring with same parameters except for wealth
        wealth ranging from the poorest person’s amount of grain to the richest person’s amount of grain
        """
        if self.is_dead(self):
            self.reset(self,
                       self.life_expectancy_min,
                       self.life_expectancy_max,
                       self.max_metabolism,
                       self.max_vision,
                       self.x,
                       self.y)
            self.wealth = random.randint(world.wealth_min, world.wealth_max)

    # TODO: moving logic


'''
    def move(self, world):
        """Core logic for navigating the world"""
        
'''
