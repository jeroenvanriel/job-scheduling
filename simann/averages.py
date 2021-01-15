from simann import SimulatedAnnealing
from experiment import Experiment
from p_functions import *

# problem defenition
m = 10 # number of machines
jobs_file = "../ptimes_normal.txt" # file that contains the jobs
instance = SimulatedAnnealing.fromFile(jobs_file, m)
runs = 40
resLocal = []
resLin = []
resLin2 = []
resExpa = []
resExp = []
resExp2a = []
resExp2 = []

for i in range(runs):
    #expLocal = instance.start(1000, localSearch, 1, 8e10, 4e12)
    #expLin = instance.start(10000, linearBadmoveAccept, 1, 8e10, 4e12)
    expLin2 = instance.start(1000000, linearBadmoveAccept, 1, 8e10, 4e12)
    #expExpa = instance.start(10000, exponentialDecay, 1, 8e10, 4e12)
    expExp = instance.start(1000000, exponentialDecay, 1, 8e10, 4e12)
    #expExp2a = instance.start(10000, exponentialDecayNonInc, 1, 8e10, 4e12)
    expExp2 = instance.start(1000000, exponentialDecayNonInc, 1, 8e10, 4e12)
    #resLocal.append(expLocal.best_makespan)
    #resLin.append(expLin.best_makespan)
    resLin2.append(expLin2.best_makespan)
    #resExpa.append(expExpa.best_makespan)
    resExp.append(expExp.best_makespan)
    #resExp2a.append(expExp2a.best_makespan)
    resExp2.append(expExp2.best_makespan)
    print(i)


#print(sum(resLocal)/runs)
#print(sum(resLin)/runs)
print(sum(resLin2)/runs)
#print(sum(resExpa)/runs)
print(sum(resExp)/runs)
#print(sum(resExp2a)/runs)
print(sum(resExp2)/runs)
