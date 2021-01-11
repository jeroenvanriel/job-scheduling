from simann import SimulatedAnnealing
from experiment import Experiment
from p_functions import *
import os, pickle
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from dataclasses import dataclass
from statistics import mean

# problem definition
m = 10 # number of machines
jobs_file = "../ptimes.txt" # file that contains the jobs
instance = SimulatedAnnealing.fromFile(jobs_file, m)

# list of lists, for the eventual results in the search grid
final_best_makespan_lst = []

# we perform hyperparameter tweaking by doing a grid search on the ranges defined below

# bad-acceptance parameter range
k_min = 10**8
k_step = 2*10**9
k_n = 40

# good-acceptance parameter range
i_min = 10**8
i_step = 2*10**8
i_n = 25

# loop through the bad-acceptance parameters
for k in range(k_n):
    best_makespan_lst = []
    
    # loop through the good-acceptance parameter
    for i in range(i_n):
        makespan_lst = []
        for j in range(2):
            accept_experiment = instance.start(3000, exponentialDecay, 0, i_min+i*i_step, k_min+k*k_step)
            makespan_lst.append(accept_experiment.best_makespan)
            print(int((i/i_n)*100)*'#')
            print(int((k/k_n)*100)*'#')
        best_makespan_lst.append(mean(makespan_lst))
        
        
    final_best_makespan_lst.append(best_makespan_lst)



fig = plt.figure(figsize=(8, 8))
gs = GridSpec(nrows=1, ncols=1)

ax0 = fig.add_subplot(gs[0, 0])
plt.title('best makespan')
heatmap = ax0.imshow(final_best_makespan_lst, extent=[0,i_n,0,k_n])
ax0.set_xticks([ i_n*(1/2 + t)/(i_n) for t in range(i_n)])
ax0.set_yticks([ k_n*(1/2 + t)/(k_n) for t in range(k_n)])
ax0.set_xticklabels(["{:.1e}".format(i_min+i*i_step) for i in range(i_n)])
ax0.set_yticklabels(["{:.1e}".format(k_min+k*k_step) for k in range(k_n)])
plt.xlabel("good move acceptance")
plt.ylabel("bad move acceptance")
plt.colorbar(heatmap)
fig.autofmt_xdate()
plt.savefig("./experiments/heatmap_exponentialdecay_given_data_zoom.png")
plt.savefig("./experiments/heatmap_exponentialdecay_given_data_zoom.pdf")
plt.show()
