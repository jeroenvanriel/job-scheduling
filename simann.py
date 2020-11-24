import math
import random
import matplotlib.pyplot as plt
import os
import pickle


# read a list of the processing times for the jobs
ptimes = []

input_file = open("ptimes.txt", "r")
for p in input_file:
  ptimes.append(int(p))

print("number of jobs in input: {}".format(len(ptimes)))

# sort list in descending order
ptimes.sort(reverse=True)

# number of jobs
n = len(ptimes)

# number of machines
m = 10


def getRandomState():
    """Returns the state after randomly assigning each job to a machine."""

    s = [-1 for x in range(n)]

    for j in range(n):
        # assign job j randomly to one of the machines
        s[j] = random.randrange(m)

    return s


def getMove(state):
    """
    Randomly determines a 'move' to a neighbor state. A move is a 3-tuple (job, current_machine, new_machine), which
    indicates that job was assigned to current_machine in the current state and will be assigned to new_machine in
    the neighboring state.
    """

    # we randomly select one of the jobs
    job = random.randrange(n)
    current_machine = state[job]

    # we randomly select a machine to move it to
    new_machine = random.randrange(m)

    while new_machine == current_machine:
        new_machine = random.randrange(m)
    
    # return the change
    return (job, current_machine, new_machine)


def makespan(state):
    """Computes the makespan of a given state."""

    # list containing the total completion time for each machine
    totals = [0 for x in range(m)]

    # loop over the jobs
    for j in range(n):
        totals[state[j]] += ptimes[j]
    
    # return the maximum completion time over all machines, which is called the makespan
    return max(totals)


def makespanAfterMove(state, move):
    """Computes the makespan of a given state, after the given move has been made."""

    (job, current_machine, new_machine) = move

    # list containing the total completion time for each machine
    totals = [0 for x in range(m)]
    
    # loop over the jobs
    for j in range(n):
        if j == job:
            totals[new_machine] += ptimes[j]
        else:
            totals[state[job]] += ptimes[job]
    
    # return the maximum completion time over all machines, which is called the makespan
    return max(totals)


def assessMove(difference, temperature):
    """Determines whether to move depending on the current temperature and makespan difference."""

    if difference < 0:
        # The makespan has improved!
        # We choose to accept this move immediately.
        # However, this is not necessary, i.e., this probability does not need to be 1.
        return True
    else:
        # In this case the makespan has not improved.
        # randomly determines if we are still going to accept depending on the temperature
        # if the temperature approaches 0, we are getting more careful, so the change
        # of still accepting gets smaller and smaller
        if random.random() < temperature * math.exp(-difference):
            return True
        else:
            return False


def getTemperature(k, nr_iterations):
    """Returns the current temperature based on the current iteration and the total number of iterations. """
    ratio = (k+1) / nr_iterations

    return 1 - ratio


# the maximum number of iterations that we are allowed to do
max_iterations = 1000

# pick an initial state
state = getRandomState()
current_makespan = makespan(state)

# keep track of the current best state and makespan
best_state = state
best_makespan = current_makespan

# initial temperature
temperature = 1

# keep track of some values in order to plot them later
makespan_lst = [ current_makespan ]
temperature_lst = []

# start the simulated annealing iterations
for k in range(max_iterations):

    # update temperature
    temperature = getTemperature(k, max_iterations)
    print("Current temperature is: {}".format(temperature))
    temperature_lst.append(temperature)

    # generate a random move to a neighboring state
    move = getMove(state)

    # compute the new makespan that we would get after making the move
    new_makespan = makespanAfterMove(state, move)

    # decide if we are going to accept this move based on the difference in the makespans
    if assessMove(new_makespan - current_makespan, temperature):
        print("Accept move!")

        # make the move
        (job, current_machine, new_machine) = move
        state[job] = new_machine
        # and update the makespan
        current_makespan = new_makespan
    else:
        print("Reject move!")
    
    print("Current makespan is: {}".format(current_makespan))
    makespan_lst.append(current_makespan)


# we are left with a final state whith a certain makespan
print("Final makespan: {}".format(current_makespan))

plt.figure()

plt.subplot(211)
plt.plot(makespan_lst)

plt.subplot(212)
plt.plot(temperature_lst)
plt.show()


# save the collected data to file
data = (makespan_lst, temperature_lst)

i = 0
while os.path.exists("./output/simann1_%s" % i):
    i += 1

with open("./output/simann1_%s" % i, "wb") as fp:
    pickle.dump(data, fp)
