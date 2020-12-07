from simann import SimulatedAnnealing
from experiment import Experiment
from p_functions import localSearch

# problem defenition
m = 10 # number of machines
jobs_file = "../ptimes.txt" # file that contains the jobs
instance = SimulatedAnnealing.fromFile(jobs_file, m)

# output filename
output_prefix = "./experiments/simann"

# run experiment and save to file
experiment1 = instance.start(1000, localSearch, 0, 0) # 1000 iterations using local search
experiment1.showResults() # show numerical summary and plots
save_file = experiment1.save(output_prefix) # save this experiment to file
print(save_file) # print the file name to which the experiment was saved

# now we load this experiment from file
experiment2 = Experiment.loadFromFile(save_file)
experiment2.showResults()

experiment2.printSchedule(instance)
experiment2.plotSchedule(instance)
