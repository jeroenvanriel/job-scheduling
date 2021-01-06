from simann import SimulatedAnnealing
from experiment import Experiment
from p_functions import *

# problem defenition
m = 10 # number of machines
jobs_file = "../ptimes.txt" # file that contains the jobs
instance = SimulatedAnnealing.fromFile(jobs_file, m)

# output filename
output_prefix = "./experiments/state_exp"

# run experiments and save their result plots to file

exp1 = instance.start(1000, localSearch, 0, 8e10, 4e12)
exp1.plotSchedule(instance, file_name="./experiments/state_exp1_schedule.pdf")

exp2 = instance.start(1000, localSearch, 1, 8e10, 4e12)
exp2.plotResults("{}2.pdf".format(output_prefix))

exp3 = instance.start(10000, linearBadmoveAccept, 1, 8e10, 4e12)
exp3.plotResults("{}3.png".format(output_prefix))

exp4 = instance.start(100000, exponentialDecay, 1, 8e10, 4e12)
exp4.plotResults("{}4.pdf".format(output_prefix))

exp5 = instance.start(100000, exponentialDecayNonInc, 1, 8e10, 4e12)
exp5.plotResults("{}5.pdf".format(output_prefix))
