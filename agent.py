"""
Turtle logic

NOTE:
1.(Not Implemented)In Netlogo's implementation, agent initial age is set to randint(0, life_expectancy_max) ???
2.(Implemented)In Netlogo's implementation, agent initial wealth is set to metabolism + randint(0, 50)
"""
import random, math


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
        self.heading = None
        self.offspring = False
        self.initialize()

    def initialize(self):
        """Sets initial status of an agent"""
        self.life_expectancy = random.randint(self.life_expectancy_min, self.life_expectancy_max)
        self.metabolism = random.randint(1, self.max_metabolism)
        self.vision = random.randint(1, self.max_vision)
        self.age = 0
        if not self.offspring:
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

    def get_wealth(self):
        """Returns wealth"""
        return self.wealth

    def reproduce(self, world):
        """
        Reproduces an offspring with same parameters except for wealth
        Wealth ranging from the poorest person’s amount of grain to the richest person’s amount of grain
        Calls initialize() to re-setup
        """
        if self.is_dead():
            self.offspring = True
            self.initialize()
            self.wealth = random.randint(world.wealth_min, world.wealth_max)

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

    def harvest(self, world):
        """Harvests grain, if multiple agents on patch, they get equal amount"""
        self.wealth += math.floor(world.get_grain(self.x, self.y) / len(world.get_agent(self.x, self.y)))
        world.harvest_grain(self.x, self.y)

    def go(self, world):
        """Agent lifecycle"""
        self.move(world)
        self.harvest(world)
        self.metabolize()
        self.aging()
        self.reproduce(world)  # Checks death condition
