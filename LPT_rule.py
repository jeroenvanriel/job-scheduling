# a list of the processing times for the jobs
ptimes = [1415926535, 8214808651, 4428810975, 7245870066, 3305727036, 9833673362, 5681271, 4201995611, 5024459455, 5982534904, 5820974944, 4811174502, 4564856692, 7892590360, 744623799, 6094370277, 1468440901, 5187072113, 7101000313, 8903894223, 8979323846, 3282306647, 6659334461, 631558817, 5759591953, 4406566430, 4526356082, 2129021960, 3469083026, 2875546873, 5923078164, 8410270193, 3460348610, 113305305, 6274956735, 539217176, 2249534301, 4999999837, 7838752886, 2858849455, 2643383279, 938446095, 2847564823, 4881520920, 921861173, 8602139494, 7785771342, 8640344181, 4252230825, 1159562863, 628620899, 8521105559, 4543266482, 4882046652, 1885752724, 2931767523, 4654958537, 2978049951, 5875332083, 9550031194, 5028841971, 5058223172, 3786783165, 9628292540, 8193261179, 6395224737, 7577896091, 5981362977, 3344685035, 8823537875, 8628034825, 6446229489, 1339360726, 1384146951, 8912279381, 8467481846, 1050792279, 597317328, 8142061717, 6252505467, 6939937510, 5359408128, 2712019091, 9171536436, 3105118548, 1907021798, 7363717872, 4771309960, 2619311881, 9375195778, 3421170679, 5493038196, 249141273, 9415116094, 8301194912, 7669405132, 6892589235, 1609631859, 7669147303, 4157424218]

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
