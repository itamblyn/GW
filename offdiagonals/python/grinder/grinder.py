#!/usr/bin/python

clean = False

diagonal_n = 180

import numpy as np
import scipy
import random
import pylab
from numpy import linalg as LA

SigmaM = np.zeros((diagonal_n,diagonal_n),dtype=np.complex)
SigmaB = np.zeros((diagonal_n,diagonal_n),dtype=np.complex)
dft = np.zeros(diagonal_n,dtype=float)

inputFileM = open('SigmaM.mat','r')
inputFileB = open('SigmaB.mat','r')
inputFileDFT = open('dft.dat','r')

for i in range(diagonal_n):

    dft[i] = float(inputFileDFT.readline().split()[1])

for i in range(diagonal_n):

    lineM = inputFileM.readline().split()
    lineB = inputFileB.readline().split()

    for j in range(diagonal_n):

        SigmaM[i][j] = np.complex(lineM[j])
        SigmaB[i][j] = np.complex(lineB[j])


for target_index in np.arange(90,96,1):

    e_coor_min_diff = 100.   # set to high number

    for energy in np.arange(-3,1,0.1):     # this should probably be some window around the DFT value

        Sigma = np.zeros((diagonal_n,diagonal_n),dtype=np.complex)
        for i in range(diagonal_n):
            for j in range(diagonal_n):
                Sigma[i][j] = SigmaM[i][j]*energy + SigmaB[i][j]

        new_eigenvalues, new_eigenvectors = LA.eig(Sigma)

        old_index = target_index
        new_index = np.argmax(new_eigenvectors[old_index])
        e_coor_diff = np.abs(np.real(new_eigenvalues[new_index]) - energy)

        if e_coor_diff < e_coor_min_diff:
            e_coor_min_diff = e_coor_diff
            cross_energy = np.real(new_eigenvalues[new_index])

    print old_index, dft[old_index], cross_energy

