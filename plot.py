import matplotlib.pyplot as plt
import csv


def plot_gini(tick, gini_index):
    if (tick[-1] % 100) == 0:
        # plot gini distribution
        plt.plot(tick, gini_index)
        plt.show()

        # plot

        gini_average = [average(gini_index)]
        print(gini_average[-1])

        with open('./gini-index_data.csv', 'a') as f:
            # create the csv writer
            writer = csv.writer(f)
            # write a row to the csv file
            # writer.writerow(gini_average)
            writer.writerow(gini_index)

def average(lst):
    return sum(lst) / len(lst)
