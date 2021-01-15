from simann import SimulatedAnnealing
from experiment import Experiment
from p_functions import *
import matplotlib.pyplot as plt

# problem defenition
m = 10 # number of machines
jobs_file = "../ptimes_normal.txt" # file that contains the jobs
instance = SimulatedAnnealing.fromFile(jobs_file, m)
runs = 100
iterations = 1000000
resLocal = []
resLocalAvg = []
resLin = []
resLinAvg = []
resExp = []
resExpAvg = []
resExp2 = []
resExp2Avg = []

for i in range(runs):
    expLocal = instance.start(iterations, localSearch, 0, 8e10, 4e12)
    resLocal.append(expLocal.makespan_lst)
    expLin = instance.start(iterations, linearBadmoveAccept, 0, 8e10, 4e12)
    resLin.append(expLin.makespan_lst)
    expExp = instance.start(iterations, exponentialDecay, 0, 8e10, 4e12)
    resExp.append(expExp.makespan_lst)
    expExp2 = instance.start(iterations, exponentialDecayNonInc, 0, 8e10, 4e12)
    resExp2.append(expExp2.makespan_lst)

for j in range(iterations):
    if (j % 1000 == 0):
        numberLocal = 0
        numberLin = 0
        numberExp = 0
        numberExp2 = 0
        for i in range(runs):
            numberLocal += resLocal[i][j]
            numberLin += resLin[i][j]
            numberExp += resExp[i][j]
            numberExp2 += resExp2[i][j]
        resLocalAvg.append(numberLocal/runs)
        resLinAvg.append(numberLin/runs)
        resExpAvg.append(numberExp/runs)
        resExp2Avg.append(numberExp2/runs)

fig = plt.figure(figsize=(12,6))
plt.plot(resLocalAvg, label='Plain local search')
plt.plot(resLinAvg, label='Linear bad-move acceptance')
plt.plot(resExpAvg, label='Exponential decay (null is good)')
plt.plot(resExp2Avg, label='Exponential decay (null is bad)')
plt.title('Average makespan')
plt.ylabel('Makespan')
plt.xlabel('Iterations')
plt.legend()
plt.show()
