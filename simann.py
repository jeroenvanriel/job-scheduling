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
            totals[state[j]] += ptimes[j]
    
    # return the maximum completion time over all machines, which is called the makespan
    return max(totals)


def assessMove(difference, temperature):
    """Determines whether to move depending on the current temperature and makespan difference."""

    if difference < 0:
        # The makespan has improved!
        # We choose to accept this move immediately.
        # However, this is not necessary, i.e., this probability does not need to be 1.
        # I think that it is even crucial to have this probability decrease if the difference is too big, i.e.,
        # if the improvement is too good. We want to make the algorithm less 'greedy'.

        if temperature > 0.90:
            return True
        else:
            return random.random() < math.exp(difference / 8e10)
    else:
        # In this case the makespan has not improved.
        # Randomly determine if we are still going to accept depending on the temperature.
        # If the temperature approaches 0, we are getting more careful, so the change
        # of still accepting gets smaller and smaller.
        # Furthermore, the larger the difference, the smaller the chance that we will accept
        # the move.
        return random.random() < temperature * math.exp(-difference / 4e12)


def getTemperature(k, nr_iterations):
    """Returns the current temperature based on the current iteration and the total number of iterations. """
    ratio = (k+1) / nr_iterations

    return 1 - ratio


# the maximum number of iterations that we are allowed to do
n_iterations = 2000000

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
# difference between t and t-1
difference_lst = [ 0 ]
# number of times that we accepted the random move
accept_nr = 0

# start the simulated annealing iterations
for k in range(n_iterations):

    # update temperature
    temperature = getTemperature(k, n_iterations)
    #print("Current temperature is: {}".format(temperature))
    temperature_lst.append(temperature)

    # generate a random move to a neighboring state
    move = getMove(state)

    # compute the new makespan that we would get after making the move
    new_makespan = makespanAfterMove(state, move)

    # decide if we are going to accept this move based on the difference in the makespans
    difference = new_makespan - current_makespan
    difference_lst.append(difference)
    
    if assessMove(difference, temperature):
        #print("Accept move!")
        accept_nr += 1

        # make the move
        (job, current_machine, new_machine) = move
        state[job] = new_machine
        # and update the makespan
        current_makespan = new_makespan
    else:
        pass
        #print("Reject move!")
    
    # update the best known values
    if current_makespan < best_makespan:
        best_makespan = current_makespan
        best_state = state
    
    #print("Current makespan is: {}".format(current_makespan))
    makespan_lst.append(current_makespan)


# we are left with a final state whith a certain makespan
print("Final makespan: {:e}".format(current_makespan))

# but we also kept track of the best makespan that we encountered so far
print("Best makespan: {:e}".format(best_makespan))

print("Accept ratio: {}".format(accept_nr / n_iterations))

plt.figure()

plt.subplot(311)
plt.title('Makespan')
plt.yscale('log')
plt.plot(makespan_lst)

plt.subplot(312)
plt.title('Temperature')
plt.yscale('linear')
plt.plot(temperature_lst)

plt.subplot(313)
plt.title('Difference')
plt.yscale('linear')
plt.plot(difference_lst)
plt.show()


# save the collected data to file
data = (best_makespan, best_state, makespan_lst, temperature_lst, difference_lst)

i = 0
while os.path.exists("./output/simann1_%s" % i):
    i += 1

with open("./output/simann1_%s" % i, "wb") as fp:
    pickle.dump(data, fp)
