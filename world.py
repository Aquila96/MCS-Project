import random

'''

'''


class World:

    def __init__(self, x, y, max_grain, percent_best_land, grain_growth_interval, num_grain_grown):
        """
        Initializes world with dimensions x, y;
        Each patch has 3-tuple: (grain-here, max-grain-here, agent)
        """
        self.x = x
        self.y = y
        self.max_grain = max_grain
        self.wealth_min = 0
        self.wealth_max = 0
        self.num_grain_grown = num_grain_grown
        # TODO: setup grain distribution & diffuse
        self.patch = [[(0, 0, None) for i in range(x)] for j in range(y)]

    def set_max_grain_here(self, x, y, max_grain_here):
        """Sets max grain of a patch"""
        self.assert_location(x, y)
        self.patch[x][y][1] = max_grain_here

    def get_max_grain_here(self, x, y):
        """Gets max grain of a patch"""
        self.assert_location(x, y)
        return self.patch[x][y][1]

    def grow_grain(self):
        """Grows grain across all patches"""
        for i in range(len(self.patch)):
            for j in range(len(self.patch[i])):
                if (self.patch[i][j][0] + self.num_grain_grown) <= self.get_max_grain_here(i, j):
                    self.patch[i][j][0] += self.num_grain_grown

    def set_grain(self, x, y, grain):
        """Sets grain of a patch"""
        self.assert_location(x, y)
        self.patch[x][y][0] = grain

    def get_grain(self, x, y):
        """Returns grain of a patch"""
        self.assert_location(x, y)
        return self.patch[x][y][0]

    def harvest_grain(self, x, y):
        """Sets grain of a patch"""
        self.assert_location(x, y)
        self.patch[x][y][0] = 0

    def set_agent(self, x, y, agent):
        """Spawns (or updates) an agent at given patch"""
        self.assert_location(x, y)
        self.patch[x][y][2] = agent

    def get_agent(self, x, y):
        """Returns an agent at given patch"""
        self.assert_location(x, y)
        return self.patch[x][y][2]

    def is_empty(self, x, y):
        """Returns boolean on whether patch is not occupied"""
        return self.patch[x][y][2] is None

    def set_wealth_range(self, wealth_min, wealth_max):
        """Updates the poorest and richest values for agent reproduction reference"""
        self.wealth_min = wealth_min
        self.wealth_max = wealth_max

    def assert_location(self, x, y):
        """Guards illegal values"""
        assert self.x >= x >= 0
        assert self.y >= y >= 0
