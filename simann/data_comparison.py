from simann import SimulatedAnnealing
from experiment import Experiment
from p_functions import *

# problem defenition
m = 10 # number of machines
jobs_file = "../ptimes_normal.txt" # file that contains the jobs
instance = SimulatedAnnealing.fromFile(jobs_file, m)

# output filename
output_prefix = "./experiments/data_exp"

# run experiments and save their result plots to file

exp1 = instance.start(100, localSearch, 0, 8e10, 4e12)
exp1.plotResults("{}1.png".format(output_prefix))
exp1.plotSchedule(instance, file_name="./experiments/data_exp1_schedule.png")

exp2 = instance.start(100, localSearch, 1, 8e10, 4e12)
exp2.plotResults("{}2.png".format(output_prefix))


exp3 = instance.start(10000, localSearch, 0, 8e10, 4e12)
exp3.plotResults("{}1.png".format(output_prefix))

exp3 = instance.start(10000, localSearch, 1, 8e10, 4e12)
exp3.plotResults("{}2.png".format(output_prefix))