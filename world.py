"""
Patches in NetLogo
NOTE: In this implementation, no agent initially spawns in the same patch
"""
import math
import random

random.seed()


# TODO: Time ticks & Growth Interval
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
        self.gini_index = 0
        self.num_grain_grown = num_grain_grown
        self.percent_best_land = percent_best_land
        self.grain_growth_interval = grain_growth_interval
        self.patches = [[[0, 0, []] for i in range(x)] for j in range(y)]
        # give some patches the highest amount of grain possible
        # these patches are the "best land"
        for i in range(len(self.patches)):
            for j in range(len(self.patches[i])):
                if random.random() <= self.percent_best_land:
                    self.set_max_grain(i, j, self.max_grain)
                    self.set_grain(i, j, self.get_max_grain(i, j))
        # spread that grain around the window a little and put a little back
        # into the patches that are the "best land" found above
        for _ in range(5):
            for i in range(len(self.patches)):
                for j in range(len(self.patches[i])):
                    if self.get_max_grain(i, j) != 0:
                        self.set_grain(i, j, self.get_max_grain(i, j))
            self.diffuse(0.25)
        # spread the grain around some more
        for _ in range(10):
            self.diffuse(0.25)
        # round grain levels to whole numbers
        for i in range(len(self.patches)):
            for j in range(len(self.patches[i])):
                self.set_grain(i, j, math.floor(self.get_grain(i, j)))
                self.set_max_grain(i, j, self.get_grain(i, j))

    def diffuse_single(self, x, y, portion):
        """Share portions of grain to neighbouring patches"""
        self.assert_location(x, y)
        assert 1 > portion > 0
        for p in self.get_neighbours8(x, y):
            self.set_grain(p[0], p[1], self.get_grain(p[0], p[1]) + portion * self.get_grain(x, y) / 8)
            self.set_grain(x, y, (1 - portion / 8) * self.get_grain(x, y))

    def diffuse(self, portion):
        """Diffuse for all non-zero patches"""
        for i in range(len(self.patches)):
            for j in range(len(self.patches[i])):
                if self.get_grain(i, j) != 0:
                    self.diffuse_single(i, j, portion)

    def get_neighbours8(self, x, y):
        """Returns 8 neighbouring patches"""
        self.assert_location(x, y)
        return [(i, j) for i in range(x - 1, x + 2)
                for j in range(y - 1, y + 2)
                if ((x != i or y != j) and
                    (0 <= i < self.x) and
                    (0 <= j < self.y))]

    def get_neighbours4(self, x, y):
        """Returns 4 neighbouring patches"""
        self.assert_location(x, y)
        return [(i, j) for i in range(x - 1, x + 2)
                for j in range(y - 1, y + 2)
                if ((x == i or y == j) and (x != i or y != j) and
                    (0 <= i < self.x) and
                    (0 <= j < self.y))]

    def set_max_grain(self, x, y, max_grain):
        """Sets max grain of a patch"""
        self.assert_location(x, y)
        self.patches[x][y] = (self.patches[x][y][0], max_grain, self.patches[x][y][2])

    def get_max_grain(self, x, y):
        """Gets max grain of a patch"""
        self.assert_location(x, y)
        return self.patches[x][y][1]

    def grow_grain(self):
        """Grows grain across all patches"""
        for i in range(len(self.patches)):
            for j in range(len(self.patches[i])):
                if (self.get_grain(i, j) + self.num_grain_grown) <= self.get_max_grain(i, j):
                    self.set_grain(i, j, self.get_grain(i, j) + self.num_grain_grown)
                else:
                    self.set_grain(i, j, self.max_grain)

    def set_grain(self, x, y, grain):
        """Sets grain of a patch"""
        self.assert_location(x, y)
        self.patches[x][y] = (grain, self.patches[x][y][1], self.patches[x][y][2])

    def get_grain(self, x, y):
        """Returns grain of a patch"""
        self.assert_location(x, y)
        return self.patches[x][y][0]

    def harvest_grain(self, x, y):
        """Sets grain of a patch"""
        self.assert_location(x, y)
        self.patches[x][y] = (0, self.patches[x][y][1], self.patches[x][y][2])

    def set_agent(self, x, y, agent):
        """Spawns (or updates) an agent at given patch"""
        self.assert_location(x, y)
        self.patches[x][y][2].append(agent)

    def unset_agent(self, x, y, agent):
        """De-spawns an agent at given patch"""
        self.assert_location(x, y)
        self.patches[x][y][2].remove(agent)

    def get_agent(self, x, y):
        """Returns a list of agents at given patch"""
        self.assert_location(x, y)
        return self.patches[x][y][2]

    def is_empty(self, x, y):
        """Returns boolean on whether patch is not occupied"""
        return len(self.get_agent(x, y)) == 0

    def list_empty_patch(self):
        """Returns a list of coordinates of patches that are not occupied"""
        lst = []
        for i in range(len(self.patches)):
            for j in range(len(self.patches[i])):
                if self.is_empty(i, j):
                    lst.append((i, j))
        return lst

    def update_wealth_range(self):
        """Updates the poorest and richest values"""
        wealth_max = 0
        wealth_min = 10000
        for i in range(len(self.patches)):
            for j in range(len(self.patches[i])):
                if not self.is_empty(i, j):
                    for agent in self.get_agent(i, j):
                        if agent.get_wealth() > wealth_max:
                            wealth_max = agent.get_wealth()
                        if agent.get_wealth() < wealth_min:
                            wealth_min = agent.get_wealth()

        self.wealth_min = wealth_min
        self.wealth_max = wealth_max

    def refresh(self):
        """Updates stats about the world, grow grains"""
        self.update_wealth_range()
        self.grow_grain()

    def assert_location(self, x, y):
        """Guards illegal values"""
        assert self.x > x >= 0
        assert self.y > y >= 0

    def update_gini_index(self, agents):

        wealth_list = [agent.get_wealth() for agent in agents]
        wealth_list.sort()

        linear_lorenz_step = self.wealth_max/len(agents)
        self.gini_index = sum([linear_lorenz_step*i - sum(wealth_list[:i]) for i in wealth_list])
