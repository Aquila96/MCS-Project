

class Result:

    def __init__(self):
        """Initialises result with lists for each metric"""
        self.tick = []
        self.wealth_min = []
        self.wealth_max = []
        self.wealth_group_low = []
        self.wealth_group_mid = []
        self.wealth_group_upper = []
        self.gini_index = []

    def load_result(self, tick, world, agents):
        """
        Loads results for the current tick
        Calculates wealth grouping and gini index
        """
        self.tick += [tick]
        self.wealth_min = world.wealth_min
        self.wealth_max = world.wealth_max
        self.__append_gini_index(world, agents)
        self.__append_wealth_grouping(agents)

    def __append_gini_index(self, world, agents):
        """Calculates gini index and appends to results"""
        wealth_list = [agent.get_wealth() for agent in agents]
        wealth_list.sort()

        linear_lorenz_step = world.wealth_max/len(agents)
        self.gini_index += [sum([linear_lorenz_step*i - sum(wealth_list[:i]) for i in wealth_list])]

    def __append_wealth_grouping(self, agents):
        low_group = 0
        mid_group = 0
        up_group = 0

        for agent in agents:
            if agent.get_wealth <= self.wealth_max[-1]/3:
                low_group += 1
            elif agent.get_wealth <= self.wealth_max[-1]*2/3:
                mid_group += 1
            else:
                up_group += 1

        self.wealth_group_low += [low_group]
        self.wealth_group_mid += [mid_group]
        self.wealth_group_upper += [up_group]