from simann import SimulatedAnnealing
from experiment import Experiment
from p_functions import *

# problem defenition
m = 2 # number of machines
jobs_file = "../ptimes_boundary.txt" # file that contains the jobs
instance = SimulatedAnnealing.fromFile(jobs_file, m)

# output filename
output_prefix = "./experiments/verification_exp"

# run experiments and save their result plots to file

exp1 = instance.start(100, localSearch, 0, 8e10, 4e12)
exp1.plotSchedule(instance, file_name="./experiments/verification_exp1_schedule.png")

exp2 = instance.start(100, localSearch, 1, 8e10, 4e12)
exp2.plotSchedule(instance, file_name="./experiments/verification_exp2_schedule.png")