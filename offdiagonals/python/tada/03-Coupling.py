#!/usr/bin/python

import sys
import numpy as np
import scipy
import random
import pylab
from numpy import linalg as LA


inputFile = open(sys.argv[1],'r')  # this gives the projection of the gas phase state onto each KS state

inputFile.readline()
inputFile.readline()

LHS_DFT = []

for line in inputFile.readlines():

    n, alpha = int(line.split()[0]) - 1, np.complex(float(line.split()[1]), float(line.split()[2]))
    LHS_DFT.append(alpha)

inputFile.close()

LHS_DFT = np.array(LHS_DFT, dtype=np.complex)

inputFile = open(sys.argv[2],'r')  # this gives the projection of the other gas phase state onto each KS state

inputFile.readline()
inputFile.readline()

RHS_DFT = []

for line in inputFile.readlines():

    n, alpha = int(line.split()[0]) - 1, np.complex(float(line.split()[1]), float(line.split()[2]))
    RHS_DFT.append(alpha)

inputFile.close()

RHS_DFT = np.array(RHS_DFT, dtype=np.complex)


####### 

diagonal_n = 180

inputFile = open(sys.argv[3],'r')

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

#for i in range(diagonal_n):

#    sum = 0.

#    for j in range(diagonal_n):

#        omega = eig_array[j]
#        sum += iprime[j][i]*omega*np.conj(iprime[j][i])
#        
#    correction += LHS_DFT[i]*sum*np.conj(RHS_DFT[i])

sum = 0

for a in range(diagonal_n):

    for b in range(diagonal_n):

        for c in range(diagonal_n):

            sum += np.conj(LHS_DFT[a])*iprime[b][a]*eig_array[b]*np.conj(iprime[b][c])*RHS_DFT[c]
#    print 100 - 100.*a/float(diagonal_n)

print sum


inputFile.close()

