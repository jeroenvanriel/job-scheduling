from simann import SimulatedAnnealing
from experiment import Experiment
from p_functions import *

# problem defenition
m = 10 # number of machines
jobs_file = "../ptimes.txt" # file that contains the jobs
instance = SimulatedAnnealing.fromFile(jobs_file, m)
runs = 40
resLocal = []
resLin = []
resExp = []
resExp2 = []

for i in range(runs):
    expLocal = instance.start(1000, localSearch, 1, 8e10, 4e12)
    expLin = instance.start(10000, linearBadmoveAccept, 1, 8e10, 4e12)
    expExp = instance.start(100000, exponentialDecay, 1, 8e10, 4e12)
    expExp2 = instance.start(100000, exponentialDecayNonInc, 1, 8e10, 4e12)
    resLocal.append(expLocal.best_makespan)
    resLin.append(expLin.best_makespan)
    resExp.append(expExp.best_makespan)
    resExp2.append(expExp2.best_makespan)

print(sum(resLocal)/runs)
print(sum(resLin)/runs)
print(sum(resExp)/runs)
print(sum(resExp2)/runs)