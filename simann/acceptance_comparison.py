from simann import SimulatedAnnealing
from experiment import Experiment
from p_functions import *
import os, pickle
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from dataclasses import dataclass
from statistics import mean


# We perform hyperparameter tweaking by doing a grid search on the ranges defined below.

# problem definition
m = 10 # number of machines
jobs_file = "../ptimes.txt" # file that contains the jobs
instance = SimulatedAnnealing.fromFile(jobs_file, m)

# grid lists, for the eventual results in the search grid
final_best_makespan_lst = []
final_ratio_lst = []

# bad-acceptance parameter range
k_min = 0
k_max = 9

# good-acceptance parameter range
i_min = 10
i_max = 20

# the number of iterations for each experiment
n_iterations = 10000

# the number of repeated experiments with the same parameters (so per pixel)
n_duplicates = 10

# loop through the bad-acceptance parameters (y-axis)
for k in range(k_min, k_max):
    best_makespan_lst = []
    ratio_lst = []
    
    # loop through the good-acceptance parameter (x-axis)
    for i in range(i_min, i_max):
        makespan_lst = []
        ratio = []

        # perform multiple runs at each pixel
        for j in range(n_duplicates):
            exp = instance.start(n_iterations, exponentialDecay, 0, 10**i, 10**k)
            makespan_lst.append(exp.best_makespan)
            ratio.append(len(exp.accepted_good_difference_lst) / len(exp.accepted_bad_difference_lst))

            print(int((i/i_max)*100)*'#')
            print(int((k/k_max)*100)*'#')
        best_makespan_lst.append(mean(makespan_lst))
        ratio_lst.append(mean(ratio))
        
    final_best_makespan_lst.append(best_makespan_lst)
    final_ratio_lst.append(ratio_lst)
    

def plotGridData(grid_data, image_id):
    fig = plt.figure(figsize=(6, 5))
    gs = GridSpec(nrows=1, ncols=1)
    ax0 = fig.add_subplot(gs[0, 0])
    plt.title('best makespan')
    heatmap = ax0.imshow(grid_data, extent=[0,1,0,1], origin='lower')
    ax0.set_xticks([t/(i_max-i_min)+1/(2*(i_max-i_min)) for t in range(i_max-i_min)])
    ax0.set_yticks([t/k_max+1/(2*k_max) for t in range(k_min, k_max)])
    ax0.set_xticklabels(["{:.0e}".format(10**i) for i in range(i_min, i_max)])
    ax0.set_yticklabels(["{:.0e}".format(10**k) for k in range(k_min, k_max)])
    plt.xlabel("good move acceptance")
    plt.ylabel("bad move acceptance")
    plt.colorbar(heatmap)
    fig.autofmt_xdate()
    plt.savefig("./experiments/heatmap_exponentialdecay_given_data" + str(image_id) + ".png")
    plt.savefig("./experiments/heatmap_exponentialdecay_given_data" + str(image_id) + ".pdf")
    plt.show()

plotGridData(final_best_makespan_lst, 0)
plotGridData(final_ratio_lst, 1)

#print(final_ratio_lst)