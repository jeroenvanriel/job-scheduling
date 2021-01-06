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
jobs_file = "../ptimes_normal.txt" # file that contains the jobs
instance = SimulatedAnnealing.fromFile(jobs_file, m)

# output filename
output_prefix = "./experiments/accept_exp"

#accept_exp1 = instance.start(100000, exponentialDecay, 0, 8e10, 4e12) #tried to use max(jobs_file) for the third entry to get the largest single processing time as good_accept, but that does not work. 
#accept_exp1.plotResults("{}1.png".format(output_prefix))

#accept_exp2 = instance.start(100000, exponentialDecayNonInc, 0, 8e10, 4e10)
#accept_exp2.plotResults("{}2.png".format(output_prefix))

#accept_exp3 = instance.start(100000, exponentialDecayNonInc, 0, 8e10, 4e12)
#accept_exp3.plotResults("{}3.png".format(output_prefix))

#accept_exp4 = instance.start(100000, exponentialDecayNonInc, 0, 8e10, 4e10)
#accept_exp4.plotResults("{}4.png".format(output_prefix))

#accept_exp5 = instance.start(100000, exponentialDecayGreedy, 0, 1e-10, 4e12)
#accept_exp5.plotResults("{}5.png".format(output_prefix))

#accept_exp6 = instance.start(100000, exponentialDecayGreedy, 0, 3e-10, 4e12)
#accept_exp6.plotResults("{}6.png".format(output_prefix))


final_best_makespan_lst = []
k_max = 20
for k in range(0, k_max):
    best_makespan_lst = []
    
    i_max = 20

    for i in range(0, i_max):
        makespan_lst = []
        for j in range(1):
            accept_experiment = instance.start(1000, exponentialDecay, 0, 10**i, 10**k)
            makespan_lst.append(accept_experiment.best_makespan)
            
            print(int((k/k_max)*100)*'#')
        best_makespan_lst.append(mean(makespan_lst))
        
        
    final_best_makespan_lst.append(best_makespan_lst)
    


fig = plt.figure(figsize=(12, 5))
gs = GridSpec(nrows=1, ncols=1)

ax0 = fig.add_subplot(gs[0, 0])
plt.title('best makespan')
#plt.yscale('log')
#plt.xscale('log')
heatmap = ax0.imshow(final_best_makespan_lst, extent=[0,1,0,1])
ax0.set_xticks([t/i_max+1/(2*i_max) for t in range(i_max)])
ax0.set_yticks([t/k_max+1/(2*k_max) for t in range(k_max)])
ax0.set_xticklabels(["{:.2e}".format(10**i) for i in range(i_max)])
ax0.set_yticklabels(["{:.2e}".format(10**k) for k in range(k_max)])
plt.xlabel("good acceptance")
plt.ylabel("bad acceptance")
plt.colorbar(heatmap)
#plt.xticks(rotation=45)
fig.autofmt_xdate()
plt.show()

