#!/usr/bin/python

import sys
import numpy as np
import scipy
import random
import pylab
from numpy import linalg as LA


inputFile = open(sys.argv[1],'r')  # this gives the projection of the HOMO onto each KS state

inputFile.readline()
inputFile.readline()

HOMO_DFT = []

for line in inputFile.readlines():

    n, alpha = int(line.split()[0]) - 1, np.complex(float(line.split()[1]), float(line.split()[2]))
    HOMO_DFT.append(alpha)

inputFile.close()

HOMO_DFT = np.array(HOMO_DFT, dtype=np.complex)

####### 

diagonal_n = 180

inputFile = open('iprime.dat','r')

eig_array = []

iprime = []

for i in range(diagonal_n):

    eig_array.append(float(inputFile.readline().split()[1]))

    iprime.append([]) 

    for j in range(diagonal_n):

        line = inputFile.readline()

        n, alpha = int(line.split()[0]) - 1, np.complex(line.split()[1])
        iprime[-1].append(alpha)


correction = 0.


for i in range(diagonal_n):

    sum = 0.

    for j in range(diagonal_n):

        omega = eig_array[j]
        sum += iprime[j][i]*omega*np.conj(iprime[j][i])
        
    correction += HOMO_DFT[i]*sum*np.conj(HOMO_DFT[i])


inputFile.close()

print np.real(correction)
