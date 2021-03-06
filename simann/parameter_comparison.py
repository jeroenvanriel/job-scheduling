from simann import SimulatedAnnealing
from experiment import Experiment
from p_functions import *
import os, pickle
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from dataclasses import dataclass
from statistics import mean
import math

# We perform hyperparameter tweaking by doing a grid search on the ranges defined below.

# problem definition
m = 10 # number of machines
jobs_file = "../ptimes.txt" # file that contains the jobs
instance = SimulatedAnnealing.fromFile(jobs_file, m)

# grid lists, for the eventual results in the search grid
final_best_makespan_lst = []
final_ratio_lst = []

# bad-acceptance parameter range
k_min = 5*10**5
k_step = 5*10**5
k_n = 20

# good-acceptance parameter range
i_min = 10**10
i_step = 10**10
i_n = 20

# the number of iterations for each experiment
n_iterations = 5000

# the number of repeated experiments with the same parameters (so per pixel)
n_duplicates = 3


# loop through the bad-acceptance parameters (y-axis)
for k in range(k_n):
    best_makespan_lst = []
    ratio_lst = []
    
    # loop through the good-acceptance parameter (x-axis)
    for i in range(i_n):
        makespan_lst = []
        ratio = []

        # perform multiple runs at each pixel
        for j in range(n_duplicates):
            exp = instance.start(n_iterations, exponentialDecay, 0, i_min+i*i_step, k_min+k*k_step)
            makespan_lst.append(exp.best_makespan)
            ratio.append(len(exp.accepted_good_difference_lst) / len(exp.accepted_bad_difference_lst))

            print(int((i/i_n)*100)*'#')
            print(int((k/k_n)*100)*'#')

        best_makespan_lst.append(mean(makespan_lst))
        ratio_lst.append(mean(ratio))
 
    final_best_makespan_lst.append(best_makespan_lst)
    final_ratio_lst.append(ratio_lst)


def plotGridData(grid_data, image_id):
    fig = plt.figure(figsize=(8, 10))
    gs = GridSpec(nrows=1, ncols=1)
    ax0 = fig.add_subplot(gs[0, 0])
    plt.title('best makespan')
    heatmap = ax0.imshow(grid_data, extent=[0,i_n,0,k_n], origin='lower')
    ax0.set_xticks([ i_n*(1/2 + t)/(i_n) for t in range(math.floor(i_n/20), i_n, max(1,math.floor(i_n/10)))])
    ax0.set_yticks([ k_n*(1/2 + t)/(k_n) for t in range(math.floor(k_n/30), k_n, max(1,math.floor(k_n/15)))])
    ax0.set_xticklabels(["{:.1e}".format(i_min+i*i_step) for i in range(math.floor(i_n/20), i_n, max(1,math.floor(i_n/10)))])
    ax0.set_yticklabels(["{:.1e}".format(k_min+k*k_step) for k in range(math.floor(k_n/30), k_n, max(1,math.floor(k_n/15)))])
    plt.xlabel("good move acceptance")
    plt.ylabel("bad move acceptance")
    plt.colorbar(heatmap)
    fig.autofmt_xdate()
    plt.savefig("./experiments/heatmap_exponentialdecay_given_data_zoom" + str(image_id) + ".png")
    plt.savefig("./experiments/heatmap_exponentialdecay_given_data_zoom" + str(image_id) + ".pdf")
    plt.show()


plotGridData(final_best_makespan_lst, 0)
#plotGridData(final_ratio_lst, 1)

#print(final_ratio_lst)