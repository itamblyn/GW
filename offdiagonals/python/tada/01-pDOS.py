#!/usr/bin/python

import sys
import numpy as np
import scipy
import random
import pylab
from numpy import linalg as LA


inputFile = open(sys.argv[1],'r')

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

inputFile = open(sys.argv[2],'r')

eig_array = []

for i in range(diagonal_n):

    eig_array.append(float(inputFile.readline().split()[1]))

    iprime = [] 

    for j in range(diagonal_n):

        line = inputFile.readline()

        n, alpha = int(line.split()[0]) - 1, np.complex(line.split()[1])
        iprime.append(alpha)

    iprime = np.array(iprime, dtype=np.complex)

#    value = np.dot(HOMO_DFT,iprime)

    summer = 0.

    for j in range(len(HOMO_DFT)):

        summer += HOMO_DFT[j]*iprime[j]   

    print eig_array[-1], np.real(summer*np.conj(summer))


inputFile.close()
