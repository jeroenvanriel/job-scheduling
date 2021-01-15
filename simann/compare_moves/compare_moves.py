import sys
sys.path.append("..") # Adds higher directory to python modules path.

from simann import SimulatedAnnealing
from experiment import Experiment
from p_functions import *
from statistics import mean

# problem defenition
m = 10 # number of machines
jobs_file = "../../ptimes.txt" # file that contains the jobs
instance = SimulatedAnnealing.fromFile(jobs_file, m)

# output filename
output_prefix = "./experiments/exp"

# run experiments and save their result plots to file

n_iterations = 1000
p_func = linearBadmoveAccept
swapAfter_lst = [3, 5, 6, 7, 8, 9, 10, 11, 12, 13]
n_exps = 100

print('n_iterations', n_iterations)
print('p_func', p_func.__name__)
print('swapAfter_lst', swapAfter_lst)
print('n_exps', n_exps)

# first no swapping
lst = []
for i in range(n_exps):
    exp_no_swap = instance.start(n_iterations, p_func, 0, 0, 0)
    lst.append(exp_no_swap.best_makespan)

print("no swapping    : {:>16.6e}".format(mean(lst)))

# then try different values of the swapAfter parameter
for swapAfter in swapAfter_lst:
    lst = []
    for i in range(n_exps):
        exp = instance.start(n_iterations, p_func, 0, 0, 0, swap_enabled=True, swap_after=swapAfter)
        lst.append(exp.best_makespan)
    
    print("swap after {:>4}: {:>16.6e}".format(swapAfter, mean(lst)))
