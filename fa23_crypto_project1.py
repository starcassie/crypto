# EDIN 01 - Cryptography
# Project 1
# Cassie Areff, Brenna Scholte

import numpy as np
import time
import math
import subprocess
from decimal import *
from operator import add

# Define B smooth value
B = 1000

# Load in prime numbers
factorbase = []
f = open('/Users/cassieareff/Downloads/prim_2_24.txt')
less = True
for line in f.readlines():
    for i in line.split():
        num = int(i)
        if num < B:
            factorbase.append(num)
        else:
            less = False
            break
    if not less:
        break
f.close()

# Shorten factorbase based on B
print("# of primes: ", len(factorbase))

# Calculate GCD
def get_gcd(x, y):
    if (x == 0):
        return y
    if (x > y):
        return get_gcd(x % y, y)
    return get_gcd(y % x, x)

# Main function, parameters: N (number to factor)
def factor_N(N):

    # Start tracking time
    start = time.time()
    # Define matrix d, holds matrix of degrees for each r ^ 2 mod N
    d = []
    # Define vector r, list of r values
    r = []

    min_rows = 250
    val = 1
    # Fill valid degrees into matrix
    while len(r) <= min_rows:
        # Calculate r
        curr_r = int(math.sqrt(val * N) + val) # can just floor overall because j is an int
        r2 = curr_r * curr_r

        # Call B Smooth Checker
        b_smooth, degrees = b_smooth_check(r2, N)

        # If B Smooth Checker returns true, continue
        if b_smooth and curr_r not in r:
            d.append(degrees)
            r.append(curr_r)
        
        for i in range(1, val + 1):
            # Calculate r
            curr_r = int(math.sqrt((val + 1) * N) + i)
            r2 = curr_r * curr_r

            # Call B Smooth Checker
            b_smooth, degrees = b_smooth_check(r2, N)

            # If B Smooth Checker returns true, continue
            if b_smooth and curr_r not in r:
                d.append(degrees)
                r.append(curr_r)

            # Calculate r
            curr_r = int(math.sqrt(i * N) + val + 1)
            r2 = curr_r * curr_r

            # Call B Smooth Checker
            b_smooth, degrees = b_smooth_check(r2, N)

            # If B Smooth Checker returns true, continue
            if b_smooth and curr_r not in r:
                # M.append(degrees % 2)
                d.append(degrees)
                r.append(curr_r)
            if len(r) > min_rows:
                break
        val += 1

    # Write to input.txt
    input = open("input.txt", "w")
    input.write(str(len(d)) + " " + str(len(d[0])) + "\n") # matrix size
    for i in range(len(d)):
        row = d[i]
        row_s = ""
        for j in row:
            row_s += str(int(j)) + " "
        input.write(row_s[0:-1] + "\n") # write row to text file

    input.close()

    # Run given C++ program
    subprocess.run("/Users/cassieareff/Downloads/a.out input.txt output.txt".split(), stdout = subprocess.DEVNULL)

    # Read in output.txt
    output = open('output.txt')

    # First line is number of solutions
    num_solutions = output.readline()

    # Iterate through vectors and save possible solutions
    for line in output.readlines():
        # Convert line to numpy array
        nums = line.split()

        # Calculate simplified version of squared mod equation values mod_val_primes ^ 2 = mod_val_rs ^ 2 mod N
        mod_val_primes = Decimal(1)
        mod_val_rs = Decimal(1)
        deg_sol = [0] * len(factorbase)

        for s in range(len(nums)):
            if nums[s] == "1":
                mod_val_rs *= r[s]
                deg_sol = list(map(add, deg_sol, d[s]))

        for i in range(len(factorbase)):
            mod_val_primes *= Decimal(factorbase[i] ** (deg_sol[i] / 2))

        # Find the gcd of the difference
        gcd = get_gcd(abs(mod_val_primes - mod_val_rs), Decimal(N))

        # If the gcd is not 1 or N then we have found a divisor
        if gcd != 1 and gcd != N:
            # Print the solutions
            print("Solutions for", N, ":", gcd, N//gcd)
            print("Time", time.time() - start)

            # Exit the while loop
            break

    getcontext().prec = 10000

# B Smooth Checker
    # return boolean if r^2 mod N is B smooth
    # B smooth can be factored as product of primes < B
def b_smooth_check(r2, N):

    val = r2 % N

    # Holds if degree for each prime is odd or even
    degrees = [0] * len(factorbase)

    # Iterate through prime #s < B
    for i in range(len(factorbase)):

        # Current degree of prime #
        curr_d = 0
        curr_prime = factorbase[i]

        while val % curr_prime == 0:
            curr_d += 1
            val //= curr_prime
        
        # Add degree of current prime
        degrees[i] = curr_d

        # If val = 1, fully factored
        if val == 1:
            return True, degrees
    
    return False, degrees

# Main Function Call
# Test numbers from description
factor_N(323)
factor_N(307561)
factor_N(31741649)
factor_N(3205837387)
factor_N(392742364277)
# Our number
factor_N(112120391182534608975671)
