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
        """Returns the state after assigning each job by the LPT rule."""

        # enumerate the jobs, which yields a list of tuples, which we sort on
        # the processing times (in the second entry) in descending order
        ptimes_enumerated = list(enumerate(self.ptimes))
        ptimes_sorted = sorted(ptimes_enumerated, key=lambda x:x[1], reverse=True)

        # the state is encoded as the assignment of jobs to machines
        state = [-1 for x in range(self.n)]

        # we keep track of the current makespan of each machine
        makespans = [0 for x in range(self.m)]

        # loop over longest processing times first
        for (j, ptime) in ptimes_sorted:
            # determine the machine with the current minimum workload
            min_i = makespans.index(min(makespans))

            # assign job j to machine m_i
            state[j] = min_i
            # update the makespans
            makespans[min_i] += ptime

        return state

    def getInsertMove(self, state):
        """
        Randomly determines an 'insert-move' to a neighbor state and the new makespan after this move.
        An insert-move is a 2-tuple (job, new_machine), which indicates that job will be assigned to
        new_machine in the neighboring state.
        Gives the new makespan after this move has been made as the second element in the tuple.
        """

        # we randomly select one of the jobs
        job = random.randrange(self.n)
        current_machine = state[job]

        # we randomly select a machine to move it to
        new_machine = random.randrange(self.m)

        while new_machine == current_machine:
            new_machine = random.randrange(self.m)
        
        move = (job, new_machine)

        new_makespan = self.makespanAfterInsertMove(state, move)

        # return the change
        return ([move], new_makespan)

    def makespanAfterInsertMove(self, state, move):
        """Computes the makespan of a given state, after the given insert-move has been made."""

        (job, new_machine) = move

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

    def getSwapMove(self, state):
        """
        Randomly determines a 'swap-move' to a neighbor state and the new makespan after this move.
        A swap-move is exchanging job1 and job2 in the schedule. It is encoded as two insert-moves.
        Gives the new makespan after this move has been made as the second element in the tuple.
        """

        # we randomly select two jobs
        job1 = random.randrange(self.n)
        job2 = random.randrange(self.n)
        while  job1 == job2:
            job2 = random.randrange(self.n)

        move1 = (job1, state[job2])
        move2 = (job2, state[job1])

        moves = [move1, move2]

        new_makespan = self.makespanAfterSwapMove(state, moves)

        # return the change
        return (moves, new_makespan)

    def makespanAfterSwapMove(self, state, move):
        """Computes the makespan of a given state, after the given swap-move has been made."""

        (job1, new_machine1) = move[0]
        (job2, new_machine2) = move[1]

        # list containing the total completion time for each machine
        totals = [0 for x in range(self.m)]

        # loop over the jobs
        for j in range(self.n):
            if j == job1:
                totals[new_machine1] += self.ptimes[j]
            elif j == job2:
                totals[new_machine2] += self.ptimes[j]
            else:
                totals[state[j]] += self.ptimes[j]

        # return the maximum completion time over all machines, which is called the makespan
        return max(totals)

    def makespan(self, state):
        """Computes the makespan of a given state."""

        # list containing the total completion time for each machine
        totals = [0 for x in range(self.m)]

        # loop over the jobs
        for j in range(self.n):
            totals[state[j]] += self.ptimes[j]

        # return the maximum completion time over all machines, which is called the makespan
        return max(totals)

    def getTemperature(self, k, n_iterations):
        """Returns the current temperature based on the current iteration and the total number of iterations. """
        ratio = (k+1) / n_iterations

        return 1 - ratio


    def start(self, n_iterations, p_function, initial_state, good_accept, bad_accept,
            swap_enabled=False,
            swap_after=0,
            state_callback=None,
            debug=False):
        '''
        n_iterations: the total number of iterations that are used
        p_function: acceptance probability function which determines wheter to accept a move based on
            the current difference and current temperature
        swap_enabled: Wheter to make swap moves or not.
        swap_after: The number of rejected moves before the algorithm turns to making swap moves only. When
            the parameter swap_enabled=True is given, the default value of swap_after (0) will make sure
            that the algorithm only performs swap moves.
        state_callback: callback function that is called with the current iteration number, current state 
            and current makespan, only use this for debugging purposes.
        debug: whether to show debugging output.

        returns an Experiment object which contains the details about the completed run
        '''

        if debug:
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

        # keep track of how many consecutive moves we reject (for switching to swap-moves)
        n_rejected = 0
        swap = False

        # start the simulated annealing iterations
        for k in range(n_iterations):
            # callback
            if state_callback:
                state_callback(k, state, current_makespan)

            # update temperature
            temperature = self.getTemperature(k, n_iterations)
            #print("Current temperature is: {}".format(temperature))
            temperature_lst.append(temperature)

            # determine wheter to make swap moves
            swap = n_rejected >= swap_after or swap

            if debug:
                print("n_rejected: {}".format(n_rejected))
                print("swap_after: {}".format(swap_after))
                print("swap: {}".format(swap))

            # generate a random move to a neighboring state and compute the new makespan we would get after
            # making this move
            if swap_enabled and swap:
                (moves, new_makespan) = self.getSwapMove(state)
            else:
                (moves, new_makespan) = self.getInsertMove(state)

            # decide if we are going to accept this move based on the difference in the makespans
            difference = new_makespan - current_makespan
            difference_lst.append(difference)
            
            if p_function(difference, temperature, good_accept, bad_accept):
                n_rejected = 0
                #print("Accept move!")
                accept_nr += 1

                # make the move(s)
                for move in moves:
                    (job, new_machine) = move
                    state[job] = new_machine

                # and update the makespan
                current_makespan = new_makespan

                # track the differences that are accepted
                if difference < 0:
                    accepted_good_difference_lst.append(difference)
                elif difference == 0:
                    accepted_zero_difference += 1
                else:
                    accepted_bad_difference_lst.append(difference)
            else:
                n_rejected += 1
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
