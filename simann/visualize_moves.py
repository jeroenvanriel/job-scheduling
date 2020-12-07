from simann import SimulatedAnnealing
from experiment import Experiment
from p_functions import localSearch

# This script is used to visualize what happens when a move is made.

m = 4 # number of machines
jobs_file = "../ptimes_small.txt" # file that contains the jobs
instance = SimulatedAnnealing.fromFile(jobs_file, m)

# this callback function plots each intermediate state during the
# simulated annealing process
def plotIntermediateSchedule(k, state, current_makespan):
    fn = "schedules/schedule_" + str(k) + ".png"
    # we do not want to scale to the current makespan, so we provide makespan_max
    Experiment._plotState(instance, state, current_makespan,
        padding=1.5,
        file_name=fn,
        makespan_max=250,
        )

# run some iterations, so we get states: initial -> after move 0 -> after move 1 -> ...
instance.start(10, localSearch, state_callback=plotIntermediateSchedule)
