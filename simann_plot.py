# This script plots a concluded experiment


import os, sys, pickle
import matplotlib.pyplot as plt


def plotData(data):
    (makespan_lst, temperature_lst) = data

    plt.figure()

    plt.subplot(211)
    plt.plot(makespan_lst)

    plt.subplot(212)
    plt.plot(temperature_lst)
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