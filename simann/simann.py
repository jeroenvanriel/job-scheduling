import random
from timeit import default_timer as timer # see https://stackoverflow.com/questions/7370801/how-to-measure-elapsed-time-in-python
from copy import deepcopy
from experiment import Experiment


class SimulatedAnnealing:

    def __init__(self, ptimes, m):
        # jobs
        self.ptimes = ptimes

        # number of jobs
        self.n = len(ptimes)

        # number of machines
        self.m = m


    @classmethod
    def fromFile(cls, filename, m):
        # read a list of the processing times for the jobs
        input_file = open(filename, "r")

        ptimes= []
        for p in input_file:
            ptimes.append(int(p))

        return cls(ptimes, m)


    def getRandomState(self):
        """Returns the state after randomly assigning each job to a machine."""

        s = [-1 for x in range(self.n)]

        for j in range(self.n):
            # assign job j randomly to one of the machines
            s[j] = random.randrange(self.m)

        return s


    def getInitialState(self):
        """Returns the state after assigning each job by the LPT rule"""

        copyptimes = deepcopy(self.ptimes)

        s = [[] for x in range(self.n)]

        min_ci = 0
        min_i = 0

        # assign a machine to each job
        for j in range(self.n):

            # reset the variables for each iteration
            max_t = 0
            max_it = 0

            # check which position has biggest makespan
            for i in range(self.n):
                if max_t < copyptimes[i]:
                    max_t = copyptimes[i]
                    max_it = i

            # assign the job with biggest makespan to machine with smallest makespan
            s[max_it] = min_i
            # set the jobs makespan to -1
            copyptimes[max_it] = -1

            # check which machine has smallest makespan
            for i in range(self.m):
                
                c_i = 0
                
                # iterate over jobs and add to makespan if assigned to this machine
                for k in range(self.n):
                    if s[k] == i:
                        c_i += self.ptimes[s[k]]

                # if makespan of this machine is smaller then replace it
                if c_i < min_ci:
                    min_ci = c_i
                    min_i = i

        return s


    def getMove(self, state):
        """
        Randomly determines a 'move' to a neighbor state. A move is a 3-tuple (job, current_machine, new_machine), which
        indicates that job was assigned to current_machine in the current state and will be assigned to new_machine in
        the neighboring state.
        """

        # we randomly select one of the jobs
        job = random.randrange(self.n)
        current_machine = state[job]

        # we randomly select a machine to move it to
        new_machine = random.randrange(self.m)

        while new_machine == current_machine:
            new_machine = random.randrange(self.m)
        
        # return the change
        return (job, current_machine, new_machine)


    def makespan(self, state):
        """Computes the makespan of a given state."""

        # list containing the total completion time for each machine
        totals = [0 for x in range(self.m)]

        # loop over the jobs
        for j in range(self.n):
            totals[state[j]] += self.ptimes[j]
        
        # return the maximum completion time over all machines, which is called the makespan
        return max(totals)


    def makespanAfterMove(self, state, move):
        """Computes the makespan of a given state, after the given move has been made."""

        (job, current_machine, new_machine) = move

        # list containing the total completion time for each machine
        totals = [0 for x in range(self.m)]
        
        # loop over the jobs
        for j in range(self.n):
            if j == job:
                totals[new_machine] += self.ptimes[j]
            else:
                totals[state[j]] += self.ptimes[j]
        
        # return the maximum completion time over all machines, which is called the makespan
        return max(totals)


    def getTemperature(self, k, n_iterations):
        """Returns the current temperature based on the current iteration and the total number of iterations. """
        ratio = (k+1) / n_iterations

        return 1 - ratio


    def start(self, n_iterations, p_function, initial_state, good_accept, bad_accept, state_callback=None):
        '''
        n_iterations: the total number of iterations that are used
        p_function: acceptance probability function which determines wheter to accept a move based on
            the current difference and current temperature
        state_callback: callback function that is called with the current iteration number, current state 
            and current makespan, only use this for debugging purposes.

        returns an Experiment object which contains the details about the completed run
        '''

        print("Number of jobs in input: {}".format(self.n))
        print("Number of machines: {}".format(self.m))
        print("Number of iterations: {}".format(n_iterations))

        # we get the current time in order to calculate the total computation time
        t0 = timer()

        # pick an initial state
        if initial_state == 0:
            state = self.getRandomState()
        else:
            state = self.getInitialState()
        current_makespan = self.makespan(state)

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
        # accepted differences for good, bad and neutral moves
        accepted_good_difference_lst = [ 0 ]
        accepted_bad_difference_lst = [ 0 ]
        accepted_zero_difference = 0
        # number of times that we accepted the random move
        accept_nr = 0

        # start the simulated annealing iterations
        for k in range(n_iterations):
            # callback
            if state_callback:
                state_callback(k, state, current_makespan)

            # update temperature
            temperature = self.getTemperature(k, n_iterations)
            #print("Current temperature is: {}".format(temperature))
            temperature_lst.append(temperature)

            # generate a random move to a neighboring state
            move = self.getMove(state)

            # compute the new makespan that we would get after making the move
            new_makespan = self.makespanAfterMove(state, move)

            # decide if we are going to accept this move based on the difference in the makespans
            difference = new_makespan - current_makespan
            difference_lst.append(difference)
            
            if p_function(difference, temperature, good_accept, bad_accept):
                #print("Accept move!")
                accept_nr += 1

                # make the move
                (job, current_machine, new_machine) = move
                state[job] = new_machine
                # and update the makespan
                current_makespan = new_makespan
                #track the differences that are accepted
                if difference < 0:
                    accepted_good_difference_lst.append(difference)
                elif difference == 0:
                    accepted_zero_difference += 1
                else:
                    accepted_bad_difference_lst.append(difference)
            else:
                pass
                #print("Reject move!")
            
            # update the best known values
            if current_makespan < best_makespan:
                best_makespan = current_makespan
                best_state = state
            
            #print("Current makespan is: {}".format(current_makespan))
            makespan_lst.append(current_makespan)

        # callback
        if state_callback:
            state_callback(k, state, current_makespan)

        # save the results from this run
        self.result = Experiment(
            runtime = timer() - t0,
            n_iterations = n_iterations,
            accept_ratio = accept_nr / n_iterations,
            final_makespan = current_makespan,
            final_state = state,
            best_makespan = best_makespan,
            best_state = best_state,
            makespan_lst = makespan_lst,
            temperature_lst = temperature_lst,
            difference_lst = difference_lst,
            accepted_good_difference_lst = accepted_good_difference_lst,
            accepted_bad_difference_lst = accepted_bad_difference_lst,
            accepted_zero_difference = accepted_zero_difference,
        )

        return self.result
