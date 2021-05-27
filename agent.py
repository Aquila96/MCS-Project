"""
Turtle logic

NOTE:
1.(Implemented)In Netlogo's implementation, agent initial age is set to randint(0, life_expectancy_max) ???
2.(Implemented)In Netlogo's implementation, agent initial wealth is set to metabolism + randint(0, 50)
3.(Implemented)In Netlogo's implementation, agent offspring initial wealth is inconsistent with the description
"""
import math
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
        self.x = x
        self.y = y
        self.wealth = None
        self.assets = 0
        self.patches = []
        self.heading = None
        self.offspring = False
        self.educated = False
        self.initialize()

    def initialize(self):
        """Sets initial status of an agent"""
        self.life_expectancy = random.randint(self.life_expectancy_min, self.life_expectancy_max)
        self.metabolism = random.randint(1, self.max_metabolism)
        self.vision = random.randint(1, self.max_vision)
        self.age = random.randint(0, self.life_expectancy_max)
        if not self.offspring:
            self.wealth = self.metabolism + random.randint(0, 50)

    def aging(self):
        """Ages"""
        self.age += 1

    def metabolize(self):
        """Metabolizes if still has grain"""
        self.wealth -= self.metabolism

    def is_dead(self, world):
        """Dies from starvation or aging"""
        if self.wealth <= 0 and self.assets > 0:
            sell = self.patches.pop()
            self.wealth += sell['price']
            self.assets -= sell['price']
            world.clear_patch_owner(sell['x'], sell['y'])
        return self.wealth <= 0 or self.age >= self.life_expectancy

    def get_wealth(self):
        """Returns wealth"""
        return self.wealth + self.assets

    def reproduce(self, world, reproduce_error, inherit):
        """
        Reproduces an offspring with same parameters except for wealth
        Wealth ranging from the poorest person’s amount of grain to the richest person’s amount of grain
        Calls initialize() to re-setup
        """
        if self.is_dead(world):
            self.offspring = True
            self.initialize()
            if not inherit:
                if reproduce_error:
                    self.wealth = 25
                    # self.wealth = self.metabolism + random.randint(0, 50)
                else:
                    self.wealth = random.randint(world.wealth_min, world.wealth_max)
            else:
                if self.wealth <= 0:
                    self.wealth = 25

    def grain_ahead(self, world, heading):
        """Returns grain count within vision"""
        total = 0
        for v in range(1, self.vision + 1):
            if heading == 0 and self.x - v > -1:
                total += world.get_grain(self.x - v, self.y)
            if heading == 90 and self.y + v < world.y:
                total += world.get_grain(self.x, self.y + v)
            if heading == 180 and self.x + v < world.x:
                total += world.get_grain(self.x + v, self.y)
            if heading == 270 and self.y - v > -1:
                total += world.get_grain(self.x, self.y - v)
        return total

    def turn_towards_grain(self, world):
        """Best heading"""
        self.heading = 0
        best_direction = 0
        best_amount = self.grain_ahead(world, 0)
        if self.grain_ahead(world, 90) > best_amount:
            best_direction = 90
        if self.grain_ahead(world, 180) > best_amount:
            best_direction = 180
        if self.grain_ahead(world, 270) > best_amount:
            best_direction = 270
        if best_amount == 0:
            self.turn_towards_random()
        else:
            self.heading = best_direction

    def turn_towards_random(self):
        """Random heading"""
        self.heading = random.choice([0, 90, 180, 270])

    def move_random(self, world):
        """Re-roll and move to random direction"""
        self.turn_towards_random()
        self.move(world)

    def update_location(self, x, y):
        """Updates location"""
        self.x = x
        self.y = y

    def move(self, world):
        """Moves to heading"""
        self.turn_towards_grain(world)
        if self.heading == 0:
            if self.x - 1 > -1:
                world.unset_agent(self.x, self.y, self)
                world.set_agent(self.x - 1, self.y, self)
                self.update_location(self.x - 1, self.y)
            else:
                self.move_random(world)
        if self.heading == 90:
            if self.y + 1 < world.y:
                world.unset_agent(self.x, self.y, self)
                world.set_agent(self.x, self.y + 1, self)
                self.update_location(self.x, self.y + 1)
            else:
                self.move_random(world)
        if self.heading == 180:
            if self.x + 1 < world.x:
                world.unset_agent(self.x, self.y, self)
                world.set_agent(self.x + 1, self.y, self)
                self.update_location(self.x + 1, self.y)
            else:
                self.move_random(world)
        if self.heading == 270:
            if self.y - 1 > -1:
                world.unset_agent(self.x, self.y, self)
                world.set_agent(self.x, self.y - 1, self)
                self.update_location(self.x, self.y - 1)
            else:
                self.move_random(world)

    def harvest(self, harvest_yield):
        """Harvests grain, if multiple agents on patch, they get equal amount"""
        #self.wealth += math.floor(world.get_grain(self.x, self.y) / len(world.get_agent(self.x, self.y)))
        #world.harvest_grain(self.x, self.y)
        self.wealth += math.floor(harvest_yield)

    def educate(self, additional_vision, education_cost):

        if not self.educated and self.wealth > education_cost * 2:
            self.educated = True
            self.vision += additional_vision
            self.wealth -= education_cost

            # Check for vision exceeding the maximum
            if self.vision > self.max_vision:
                self.vision = self.max_vision

    def buy_land(self, world):
        free = world.get_ownerless_patches()
        for patch in free:
            if self.wealth > patch['price'] + 100:
                self.patches += [patch]
                self.assets += patch['price']
                self.wealth -= patch['price']
                world.set_patch_owner(patch['x'], patch['y'], self)

