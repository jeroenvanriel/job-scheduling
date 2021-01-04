from simann import SimulatedAnnealing
from experiment import Experiment
from p_functions import *

# problem defenition
m = 10 # number of machines
jobs_file = "../ptimes.txt" # file that contains the jobs
jobs_file_small = "../ptimes_small.txt"
instance100 = SimulatedAnnealing.fromFile(jobs_file, 100)
instance = SimulatedAnnealing.fromFile(jobs_file, m)
instance_small = SimulatedAnnealing.fromFile(jobs_file_small, 11)

# output filename
output_prefix = "./experiments/random_exp"

# run experiments and save their result plots to file

#exp1 = instance100.start(1, localSearch, 1, 8e10, 4e12)
#exp1.plotSchedule(instance100, file_name="./experiments/random_exp1_schedule.png")

#exp2 = instance.start(10000000, localSearch, 1, 8e10, 4e12)
#exp2.plotResults("{}2.png".format(output_prefix))

#exp3 = instance_small.start(1, localSearch, 1, 8e10, 4e12)
#exp3.plotSchedule(instance_small, file_name="./experiments/random_exp3_schedule.png")

exp4 = instance_small.start(1, localSearch, 1, 8e10, 4e12)
exp4.plotSchedule(instance_small, file_name="./experiments/random_exp4_schedule.png")

