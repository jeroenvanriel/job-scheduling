# Job Scheduling
This repository contains some implementation of algorithms for solving makespan scheduling problem. This project was done as part of the course Mathematical Modelling (2WH30) at TUe.


## Simulated annealing

[Wikipedia article](https://en.wikipedia.org/wiki/Simulated_annealing)

The script `simann.py` performs simulated annealing and stores the results from an experiment in an output file in the folder `output/`. The data format of these files may change over time and is described below.

### Data formats

Output data version 1, file name starting with `simann1_`
```
data = (best_makespan, best_state, makespan_lst, temperature_lst, difference_lst)
```
