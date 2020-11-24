# This script plots a concluded experiment


import os, sys, pickle
import matplotlib.pyplot as plt

def printAssignment(data):
    (best_makespan, best_state, makespan_lst, temperature_lst, difference_lst) = data

    # read a list of the processing times for the jobs
    ptimes = []

    input_file = open("ptimes.txt", "r")
    for p in input_file:
        ptimes.append(int(p))

    n = len(best_state)
    m = 10

    # For each machine we create a list that contains the jobs that have
    # been assigned to it.
    machine_jobs = [[] for x in range(m)]
    for job in range(n):
        machine_jobs[best_state[job]].append(job)

    # we print all the jobs that are assigned to each machine
    for machine in range(m):
        total = 0
        for job in machine_jobs[machine]:
            total += ptimes[job]

        print("Machine {}: (total {}) {}".format(machine, total, machine_jobs[machine]))

    print("Makespan: {:e}".format(best_makespan))


def plotData(data):
    (best_makespan, best_state, makespan_lst, temperature_lst, difference_lst) = data

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
            printAssignment(data)
            plotData(data)
        else:
            print("Cannot load data from file.")
else:
    print("Cannot find the specified file.")