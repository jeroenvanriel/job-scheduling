import os, pickle
import matplotlib.pyplot as plt
from dataclasses import dataclass


@dataclass
class Experiment:
    '''
    This class contains the results from a certain experiment run.
    It also contains some helper function to visualize the results.
    '''

    runtime: float
    accept_ratio: float
    
    final_makespan: int
    final_state: list
    
    best_makespan: int
    best_state: list

    makespan_lst: list
    temperature_lst: list
    difference_lst: list

    @classmethod
    def loadFromFile(cls, file_path):
        '''Load a past experiment from file.'''
        if not os.path.exists(file_path):
            print("Path does not exist!")       

        with open(file_path, "rb") as fp:
            data = pickle.load(fp)
            
            if data is not None:
                return data
            else:
                print("Cannot load result data from file.")


    def save(self, path):
        '''
        Save this experiment to file.
        Automatically append an increasing number to the filename.
        Returns the path of the file that was created.
        '''

        i = 0
        while os.path.exists("{}{}".format(path, i)):
            i += 1
        
        filename = "{}{}".format(path, i)

        with open(filename, "wb") as fp:
            pickle.dump(self, fp)
        
        return filename


    def showResults(self):
        '''
        This method prints a summary of the experiment and plots the makespan, temperature
        and difference values over time.
        '''

        print("Total computation (wall-clock) time: {} seconds".format(self.runtime))
        print("Final makespan: {:e}".format(self.final_makespan))
        print("Best makespan: {:e}".format(self.best_makespan))
        print("Overall accept ratio: {}".format(self.accept_ratio))
        print()

        plt.figure()

        plt.subplot(211)
        plt.title('Makespan')
        plt.yscale('log')
        plt.plot(self.makespan_lst)

        plt.subplot(212)
        plt.title('Difference')
        plt.yscale('linear')
        plt.plot(self.difference_lst)

        # plt.subplot(313)
        # plt.title('Temperature')
        # plt.yscale('linear')
        # plt.plot(self.temperature_lst)
        
        plt.tight_layout()
        plt.show()


    def printSchedule(self, problem):
        '''
        This function can print the assignment of the best schedule that was found during this
        experiment. In order to avoid problem data duplication, this method needs a reference
        to the original problem instance (of type SimulatedAnnealing) to access the ptimes.
        '''

        # For each machine we create a list that contains the jobs that have
        # been assigned to it.
        machine_jobs = [[] for x in range(problem.m)]
        for job in range(problem.n):
            machine_jobs[self.best_state[job]].append(job)

        # we print all the jobs that are assigned to each machine
        for machine in range(problem.m):
            total = 0
            for job in machine_jobs[machine]:
                total += problem.ptimes[job]

            print("Machine {}: (total {}) {}".format(machine, total, machine_jobs[machine]))

        print("Makespan: {:e}".format(self.best_makespan))


    def plotSchedule(self, problem):
        '''
        Makes a sort of 'Gantt-chart' for the best schedule that was found during this experiment.
        In order to avoid problem data duplication, this method needs a reference
        to the original problem instance (of type SimulatedAnnealing) to access the ptimes.
        '''

        # For each machine we create a list that contains the jobs that have
        # been assigned to it.
        machine_jobs = [[] for x in range(problem.m)]
        for job in range(problem.n):
            machine_jobs[self.best_state[job]].append(job)

        # Declaring a figure "gnt"
        fig, gnt = plt.subplots()

        # chart settings
        x_limit = 260
        padding = 0.5

        gnt.set_xlim(0, x_limit + 10)
        gnt.set_ylabel('Machine')

        # setting tick for max makespan
        gnt.set_xticks([x_limit])
        gnt.set_xticklabels(['maximum makespan'])

        # setting ticks for machine id's
        gnt.set_yticks([5 * (x) + 2 for x in range(problem.m)])
        gnt.set_yticklabels([str(x + 1) for x in range(problem.m)])

        gnt.grid(True) # show grid

        for machine in range(problem.m):
            blocks = []

            t = 0 # current start time
            for job in machine_jobs[machine]:
                # define scaled length
                length = problem.ptimes[job] / self.best_makespan * x_limit

                blocks.append((t + padding, length - padding))
                t += length

            # Declaring a bar in schedule
            gnt.broken_barh(blocks, (5 * machine, 4), facecolors =('tab:orange'))

        plt.show()
