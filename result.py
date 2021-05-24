import plot


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
        self.lorenz_line = []

    def load_result(self, tick, world, agents):
        """
        Loads results for the current tick
        Calculates wealth grouping and gini index
        """
        self.tick += [tick] if len(self.tick) < 1 else [self.tick[-1] + tick]
        self.wealth_min += [world.wealth_min]
        self.wealth_max += [world.wealth_max]
        self.__append_gini_index(world, agents)
        self.__append_wealth_classes(agents)

    def __append_gini_index(self, world, agents):
        """Calculates gini index and appends to results"""

        # Update the world wealth ranges
        world.update_wealth_range()

        # Get a list of the wealth of each agent and sort
        wealth_list = [agent.get_wealth() for agent in agents]
        wealth_list.sort()

        # Calculate the total wealth in the system, and the area under a linear wealth distribution
        total_wealth = sum(wealth_list)
        linear_lorenz_area = total_wealth * len(agents) / 2

        # Convert the wealth list into a cumulative wealth list (lorenz curve), and append to results
        lorenz_line = [sum(wealth_list[:i + 1]) for i in range(len(wealth_list))]
        self.lorenz_line += [lorenz_line]

        # Calculate the Gini Index, and append to results
        self.gini_index += [(linear_lorenz_area - sum(lorenz_line)) / linear_lorenz_area]

        # self.gini_index += [sum( i/len(agents)-sum(wealth_list[:i+1])/total_wealth for i in range(len(agents)) )]

    def __append_wealth_classes(self, agents):
        low_class = 0
        mid_class = 0
        up_class = 0

        for agent in agents:
            if agent.get_wealth() <= self.wealth_max[-1] / 3:
                low_class += 1
            elif agent.get_wealth() <= self.wealth_max[-1] * 2 / 3:
                mid_class += 1
            else:
                up_class += 1

        self.wealth_class_low += [low_class]
        self.wealth_class_mid += [mid_class]
        self.wealth_class_upper += [up_class]

    def stepwise_report(self):
        """Outputs result of each tick"""
        print('{}, {}, {}, {}, {:2.2}'.format(self.tick[-1],
                                              self.wealth_class_low[-1],
                                              self.wealth_class_mid[-1],
                                              self.wealth_class_upper[-1],
                                              self.gini_index[-1]))

        plot.plot_gini(self.tick, self.gini_index)

        return self.tick[-1], \
               self.wealth_min[-1], \
               self.wealth_max[-1], \
               self.wealth_class_low[-1], \
               self.wealth_class_mid[-1], \
               self.wealth_class_upper[-1], \
               self.gini_index[-1]
