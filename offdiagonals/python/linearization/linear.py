#!/usr/bin/python

diagonal_n = 180
outrange = diagonal_n
energy = -2.5

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


Sigma = np.zeros((diagonal_n,diagonal_n),dtype=np.complex)

for i in range(diagonal_n):
    for j in range(diagonal_n):
        Sigma[i][j] = SigmaM[i][j]*energy + SigmaB[i][j]

new_eigenvalues, new_eigenvectors = LA.eig(Sigma)

for j in range(outrange):

    print '# ', np.real(new_eigenvalues[j]), ' eV'

    for i in range(outrange):

       print i + 1, new_eigenvectors[i][j]

