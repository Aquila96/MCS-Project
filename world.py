import random

'''

'''


class World:

    def __init__(self, x, y):
        """
        Initialize world with dimensions x, y;
        Each patch has 3-tuple: (grain-here, max-grain-here, agent)
        """
        self.x = x
        self.y = y
        self.patch = [[(0, 0, None) for i in range(x)] for j in range(y)]

    def set_max_grain(self, x, y, max_grain):
        """Set max grain of a patch"""
        self.assert_location(x, y)
        self.patch[x][y][1] = max_grain

    def set_grain(self, x, y, grain):
        """Set grain of a patch"""
        self.assert_location(x, y)
        self.patch[x][y][0] = grain

    def set_agent(self, x, y, agent):
        """Spawns an agent at given patch"""
        self.assert_location(x, y)
        self.patch[x][y][2] = agent

    def get_agent(self, x, y):
        """Returns an agent at given patch"""
        self.assert_location(x, y)
        return self.patch[x][y][2]

    def is_empty(self, x, y):
        """Returns boolean on whether patch is not occupied"""
        return self.patch[x][y][2] is None

    def assert_location(self, x, y):
        """Guards illegal values"""
        assert self.x >= x >= 0
        assert self.y >= y >= 0
