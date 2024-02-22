# EDIN 01 - Cryptography
# Project 3
# Cassie Areff, Brenna Scholte

import itertools
import copy

# Keystream z1, z2, ... zN
z = list("0111011010111000010001111111111011110000010111111001111011101011111100000000110000011001011111000001000110000000001111011011101011111011101100010001101011101011111010100000101110011111100101000")
z = [int(i) for i in z]

# LFSR lengths
L1 = 13
L2 = 15
L3 = 17

# Feedback/connection polynomials
C13 = (list("1101011001101"))
C13 = [int(i) for i in C13]

C15 = list("010101100110101")
C15 = [int(i) for i in C15]

C17 = list("01011001010010011")
C17 = [int(i) for i in C17]


def findKey(poly, z):
    best_p = 0
    best_start = 0

    # Set start value
    values = [1, 0]
    for start in itertools.product(values, repeat=len(poly)):
        start = list(start)
        # LFSR output
        u = LFSRoutput(poly, z, start)

        # Caclulate # matching with keysteam
        diff = findDiff(u, z)

        # Calculate p = 1 - (# differences / N)
        p = 1 - (diff / len(z))

        if (p > best_p):
            best_p = p
            best_start = start
        
    return best_start


def LFSRoutput(poly, z, start):

    # Reorder poly
    new_poly = copy.deepcopy(start)
    # final_poly = poly[start:] + poly[:start]

    # While loop to concatenate copy of poly to the end until same length or greater than z
    for i in range(len(poly), len(z)):
        val = 0
        for l in range(len(poly)):
            val += poly[l] * new_poly[i - l - 1] # is i - l - 1 because the indexing starts at 0
        val = val % 2
        new_poly.append(val)

    # Return poly that is exactly the same length of z
    return new_poly

def findDiff(poly, z):
    diff = 0

    for i in range(len(poly)):
        if poly[i] != z[i]:
            diff += 1

    return diff


K1 = findKey(C13, z)
K2 = findKey(C15, z)
K3 = findKey(C17, z)

print("Key 1: ", K1)
print("Key 2: ", K2)
print("Key 3: ", K3)

output_K1 = LFSRoutput(C13, z, K1)
output_K2 = LFSRoutput(C15, z, K2)
output_K3 = LFSRoutput(C17, z, K3)

keystream = []

for i in range(len(output_K1)):
    if output_K1[i] + output_K2[i] + output_K3[i] >= 2:
        keystream.append(1)
    else:
        keystream.append(0)

if keystream == z:
    print("correct keys")
else:
    print("incorrect keys")