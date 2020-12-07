from simann import SimulatedAnnealing
from experiment import Experiment
from p_functions import *

# problem defenition
m = 10 # number of machines
jobs_file = "../ptimes.txt" # file that contains the jobs
instance = SimulatedAnnealing.fromFile(jobs_file, m)

# output filename
output_prefix = "./experiments/exp"

# run experiments and save their result plots to file

exp1 = instance.start(1000, localSearch, 8e10, 4e12)
exp1.plotResults("{}1.png".format(output_prefix))
exp1.plotSchedule(instance, file_name="./experiments/exp1_schedule.png")

exp2 = instance.start(1000, linearBadmoveAccept, 8e10, 4e12)
exp2.plotResults("{}2.png".format(output_prefix))


exp3 = instance.start(10000, localSearch, 8e10, 4e12)
exp3.plotResults("{}3.png".format(output_prefix))

exp4 = instance.start(10000, linearBadmoveAccept, 8e10, 4e12)
exp4.plotResults("{}4.png".format(output_prefix))


exp5 = instance.start(100000, exponentialDecay, 8e10, 4e12)
exp5.plotResults("{}5.png".format(output_prefix))

exp6 = instance.start(100000, exponentialDecayNonInc, 8e10, 4e12)
exp6.plotResults("{}6.png".format(output_prefix))
