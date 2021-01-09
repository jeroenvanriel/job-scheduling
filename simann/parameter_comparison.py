from simann import SimulatedAnnealing
from experiment import Experiment
from p_functions import *
import os, pickle
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from dataclasses import dataclass
from statistics import mean

# problem defenition
m = 10 # number of machines
jobs_file = "../ptimes.txt" # file that contains the jobs
instance = SimulatedAnnealing.fromFile(jobs_file, m)





final_best_makespan_lst = []
k_min = 10**9
k_max = 3*10**10
k_step = 10**9
for k in range(k_min, k_max, k_step):
    best_makespan_lst = []
    
    i_min = 10**8
    i_max = 5*10**9
    i_step = 10**8

    for i in range(i_min, i_max, i_step):
        makespan_lst = []
        for j in range(1):
            accept_experiment = instance.start(1000, exponentialDecay, 0, i, k)
            makespan_lst.append(accept_experiment.best_makespan)
            
            print(int((k/k_max)*100)*'#')
        best_makespan_lst.append(mean(makespan_lst))
        
        
    final_best_makespan_lst.append(best_makespan_lst)
    


fig = plt.figure(figsize=(12, 5))
gs = GridSpec(nrows=1, ncols=1)

ax0 = fig.add_subplot(gs[0, 0])
plt.title('best makespan')
heatmap = ax0.imshow(final_best_makespan_lst, extent=[0,5,0,3])
ax0.set_xticks([5*t/i_max + 5/(2*i_max) for t in range(i_min, i_max, 2*i_step)])
ax0.set_yticks([3*t/k_max + 3/(2*k_max) for t in range(k_min, k_max, k_step)])
ax0.set_xticklabels(["{:.1e}".format(i) for i in range(i_min, i_max, 2*i_step)])
ax0.set_yticklabels(["{:.1e}".format(k) for k in range(k_min, k_max, k_step)])
plt.xlabel("good move acceptance")
plt.ylabel("bad move acceptance")
plt.colorbar(heatmap)
fig.autofmt_xdate()
plt.savefig("./experiments/heatmap_exponentialdecay_given_data_zoom.png")
plt.savefig("./experiments/heatmap_exponentialdecay_given_data_zoom.pdf")
plt.show()