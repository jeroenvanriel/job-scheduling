# This file can be used to define different acceptance probability functions.
# The parameters that are availabe are difference (between new makespan and current makespan)
# and the current temperature.

import random, math

def localSearch(difference, temperature):
    """Only accepts good-moves."""
    if difference <= 0: # good-move
        return True
    else: # bad-move
        return False

def linearBadmoveAccept(difference, temperature):
    """Always accept good moves, and let bad-move acceptance depend linearly on the temperature."""
    if difference <= 0: # good-move
        return True
    else: # bad-move
        # Let the probability of accepting depend linearly on the temperature
        return random.random() < temperature

def exponentialDecay(difference, temperature):
    """Use an exponential function of the difference."""
    if difference < 0: # good-move
        # If the improvement is too good. We want to make the algorithm less 'greedy'.
        return random.random() < math.exp(difference / 8e10)
    else: # bad-move
        # If the temperature approaches 0, we are getting more careful, so the change
        # of still accepting gets smaller and smaller.
        # Furthermore, the larger the difference, the smaller the chance that we will accept the move.
        return random.random() < temperature * math.exp(-difference / 4e12)

def exponentialDecayNonInc(difference, temperature):
    """Use an exponential function of the difference."""
    if difference <= 0: # good-move
        # If the improvement is too good. We want to make the algorithm less 'greedy'.
        return random.random() < math.exp(difference / 8e10)
    else: # bad-move
        # If the temperature approaches 0, we are getting more careful, so the change
        # of still accepting gets smaller and smaller.
        # Furthermore, the larger the difference, the smaller the chance that we will accept the move.
        return random.random() < temperature * math.exp(-difference / 4e12)
