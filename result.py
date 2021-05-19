

class Result:

    def __init__(self):
        """Initialises result with lists for each metric"""
        self.tick = []
        self.wealth_min = []
        self.wealth_max = []
        self.wealth_class_low = []
        self.wealth_class_mid = []
        self.wealth_class_upper = []
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
        self.__append_wealth_classes(agents)

    def __append_gini_index(self, world, agents):
        """Calculates gini index and appends to results"""
        wealth_list = [agent.get_wealth() for agent in agents]
        wealth_list.sort()

        linear_lorenz_step = world.wealth_max/len(agents)
        self.gini_index += [sum([linear_lorenz_step*i - sum(wealth_list[:i]) for i in wealth_list])]

    def __append_wealth_classes(self, agents):
        low_class = 0
        mid_class = 0
        up_class = 0

        for agent in agents:
            if agent.get_wealth <= self.wealth_max[-1]/3:
                low_class += 1
            elif agent.get_wealth <= self.wealth_max[-1]*2/3:
                mid_class += 1
            else:
                up_class += 1

        self.wealth_class_low += [low_class]
        self.wealth_class_mid += [mid_class]
        self.wealth_class_upper += [up_class]