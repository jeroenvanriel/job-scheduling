# generate a list of n jobs, with times normally distributed.
import numpy as np
from typing import List, Tuple, Set, Dict, Iterable
import random
def ptimes_generate(n: int, mu: float, sigma: float, file_name: str) -> List[int]:
    """Create a list containing n jobs, with job times sampled from a normal
    distribution with mean = mu and standard deviation = sigma.
    """
    ptimes = []
    for i in range(n):
        value = np.random.normal(mu,sigma)
        value_str = str(value)
        ptimes.append(value_str)
    with open(file_name, 'w') as f:
        f.write('\n'.join(ptimes))
        
