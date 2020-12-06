from simann import SimulatedAnnealing
from experiment import Experiment
from p_functions import *

# problem defenition
m = 10 # number of machines
jobs_file = "../ptimes.txt" # file that contains the jobs
instance = SimulatedAnnealing.fromFile(jobs_file, m)

# output filename
output_prefix = "./experiments/accept_exp"

accept_exp1 = instance.start(100000, exponentialDecay, 9.8e9, 4e12) #tried to use max(jobs_file) for the third entry to get the largest single processing time as good_accept, but that does not work. 
accept_exp1.plotResults("{}1.png".format(output_prefix))

accept_exp2 = instance.start(100000, exponentialDecayNonInc, 8e10, 4e12)
accept_exp2.plotResults("{}2.png".format(output_prefix))


