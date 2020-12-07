from simann import SimulatedAnnealing
from experiment import Experiment
from p_functions import *

# problem defenition
m = 10 # number of machines
jobs_file = "../ptimes.txt" # file that contains the jobs
instance = SimulatedAnnealing.fromFile(jobs_file, m)

# output filename
output_prefix = "./experiments/first_comparison/"

# run experiments and save their result plots to file

exp1 = instance.start(10000, localSearch, 0, 0)
exp1.plotResults("{}localsearch.png".format(output_prefix))
exp1.plotSchedule(instance, file_name="{}localsearch_schedule.png".format(output_prefix))

exp2 = instance.start(10000, linearBadmoveAccept, 0, 0)
exp2.plotResults("{}linearBadmoveAccept.png".format(output_prefix))
exp2.plotSchedule(instance, file_name="{}linearBadmoveAccept_schedule.png".format(output_prefix))

exp3 = instance.start(10000, exponentialDecay, 10e10, 4e12)
exp3.plotResults("{}exponentialDecay.png".format(output_prefix))
exp3.plotSchedule(instance, file_name="{}exponentialDecay_schedule.png".format(output_prefix))
