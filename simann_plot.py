# This script plots a concluded experiment


import os, sys, pickle
import matplotlib.pyplot as plt


def plotData(data):
    data = (best_makespane, best_state, makespan_lst, temperature_lst, difference_lst)

    plt.figure()

    plt.subplot(311)
    plt.title('Makespan')
    plt.yscale('log')
    plt.plot(makespan_lst)

    plt.subplot(312)
    plt.title('Temperature')
    plt.yscale('linear')
    plt.plot(temperature_lst)

    plt.subplot(313)
    plt.title('Difference')
    plt.yscale('linear')
    plt.plot(difference_lst)
    plt.show()


fn = sys.argv[1]
if os.path.exists(fn):
    with open(fn, "rb") as fp:
        data = pickle.load(fp)
        
        if data is not None:
            plotData(data)
        else:
            print("Cannot load data from file.")
else:
    print("Cannot find the specified file.")