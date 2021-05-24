import matplotlib.pyplot as plt


def plot_gini(tick, gini_index):
    if (tick[-1] % 100) == 0:
        plt.plot(tick, gini_index)
        plt.show()
