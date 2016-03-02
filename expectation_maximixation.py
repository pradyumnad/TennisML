#! /usr/bin/env python

import numpy as np


def coin_tosses(n, p):
    """

    :param n: number of coin tosses
    :param p: probability the coin comes up heads
    :return: list of coin tosses, where True represents heads, False represents tails
    """

    return [np.random.uniform(0, 1) <= p for i in range(n)]


def validate_integer_input(prompt, value=0):
    """
    Validates that the user's input is in fact greater than some integer.
    :param prompt:
    :param value: value that the user input needs to be greater than.
    :return:
    """

    error_message = "Enter an integer value greater than {}.".format(value)

    while True:
        user_value = raw_input(prompt)
        try:
            int_value = int(user_value)
            if float(user_value) != int_value:
                print(error_message)
        except ValueError:
            print(error_message)
            continue
        if int_value > value:
            return int_value
        else:
            print(error_message)

def validate_coin_prob_input(prompt):
    """
    Validates that the probability for the coin coming up heads is a valid
    probability.

    :param prompt: message to print to the user.
    :return: validated probability the coin comes up heads.
    """

    error_message = "The probability must be a numerical value " \
                    "between 0 and 1."

    while True:
        user_value = raw_input(prompt)
        try:
            float_value = float(user_value)
        except ValueError:
            print(error_message)
            continue
        if 0 <= float_value <= 1:
            return float_value
        else:
            print(error_message)

def expectation_maximization(tosses):
	# get random value for p1 and p2
	p1 = np.random.uniform(0, 1)
	p2 = np.random.uniform(0, 1)

	num_iterations = 1
	while True:
		# initialize variables to store the number of heads and tails each coin
	    # will be responsible for as the algorithm goes
	    heads_1 = 0
	    tails_1 = 0
	    heads_2 = 0
	    tails_2 = 0
	    for trial in tosses:
	    	# calculate the likelihood that the trial came from each given coin
	    	# print trial
	    	heads = float(sum(trial))
	    	tails = float(len(trial) - sum(trial))

	    	likelihood_1 = p1**(heads) * (1-p1)**(tails)
	    	likelihood_2 = p2**(heads) * (1-p2)**(tails)

	    	# Calculate how much each coin is likely to be responsible for this trial
	    	try:
	    		credit_1 = likelihood_1 / (likelihood_1 + likelihood_2)
	    		credit_2 = likelihood_2 / (likelihood_1 + likelihood_2)
	    	except ZeroDivisionError:
	    		print("Please choose a smaller number of coin flips per trial. "\
                      "The number you have chosen is so large that the likelihoods "\
                      "are being rounded to zero by Python.")
	    		exit()
	    	
	    	# use this to determine how many coin flips are assigned to that coin
	    	heads_1 += heads * credit_1
	    	tails_1 += tails * credit_1
	    	heads_2 += heads * credit_2
	    	tails_2 += tails * credit_2

	    # now that all the trials are done and the likely heads and tails have been
	    # calculated for each coin, we can determine the new values of p1 and p2
	    new_p1 = heads_1 / (heads_1 + tails_1)
	    new_p2 = heads_2 / (heads_2 + tails_2)

	    # We keep doing this until it converges. This doesn't always happen
	    # exactly, especially if we have a large number of trials, so we can
	    # make it stop once the change is very small.
	    if abs(new_p1 - p1) < 0.00000001 and abs(new_p2 - p2) < 0.00000001:
	    	print("The final values are:\n" \
	    		  "p1: {}\n"\
	    		  "p2: {}\n" \
	    		  "It took {} iterations to find " \
	    		  "these values".format(round(p1, 3), round(p2, 3), num_iterations))

	    	break
	    else:
	    	p1 = new_p1
	    	p2 = new_p2
	    	num_iterations += 1


def main():
    trials = validate_integer_input("Enter the number of trials: ", 1)
    n = validate_integer_input("Enter the number of times the "
                               "coin is flipped in each trial: ")

    p1 = validate_coin_prob_input("Enter the probability the first "
                                  "coin turns up heads: ")

    p2 = validate_coin_prob_input("Enter the probability the second "
                                  "coin turns up heads: ")

    toss_prob = {1: p1, 2: p2}

    # We now want to create the trials our algorithm will use.
    # We will randomly assign each trial to a coin.
    coin_choice = np.random.randint(1, 3, trials) # 3 is not included
    # make sure each coin gets tossed at least once
    while 1 not in coin_choice or 2 not in coin_choice:
        coin_choice = np.random.randint(1, 3, trials)

    tosses = [coin_tosses(n, toss_prob[c]) for c in coin_choice]

    # Now we can use the algorithm.
    expectation_maximization(tosses)


if __name__ == "__main__":
    main()

