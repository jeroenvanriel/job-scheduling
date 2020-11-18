# read a list of the processing times for the jobs
ptimes = []

input_file = open("ptimes.txt", "r")
for p in input_file:
  ptimes.append(int(x))

print("number of jobs in input: {}".format(len(ptimes)))

# sort list in descending order
ptimes.sort(reverse=True)

# number of machines
m = 10

# make a list of m empty lists
# each machine gets a list of currently assigned jobs
machine_jobs = [[] for x in range(m)] 

# keep track of which jobs are assigned to which machines already
# pick the machine with the lowest current workload as the next machine to
# assign the next job to

# keep track of the minimum current workload
min_ci = 0
# and also keep track of which machine attains this minimum workload
# (as a first choice, we can pick any machine, so for convenience we just pick the first)
min_i = 0


# assign jobs following the Longest Processing Time (LPT) rule.
for p in ptimes:
    # add the current job to the machine which has the current minimum workload
    machine_jobs[min_i].append(p)

    # determine the machine with the current minimum workload
    min_ci = sum(machine_jobs[min_i])
    for i in range(m):
        c_i = sum(machine_jobs[i])
        if c_i < min_ci:
            min_ci = c_i
            min_i = i

# compute the makespan
makespan = 0
for i in range(m):
    print(machine_jobs[i])

    c_i = sum(machine_jobs[i])

    print(c_i)

    if c_i > makespan:
        makespan = c_i
    
print(makespan)
