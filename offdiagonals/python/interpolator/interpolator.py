#!/usr/bin/python
energy = '2eV'


debug_print = False

HOMO_index = 94 - 1 # band index starts from 1 for BerkeleyGW

diagonal_n = 180

import numpy as np
import scipy
import random
import pylab
from numpy import linalg as LA



inputFile = open('eig0.' + energy + '.dat','r')

eqp = np.zeros(diagonal_n, dtype=complex)

E_GW = np.zeros(diagonal_n, dtype=float)
E_GGA = np.zeros(diagonal_n, dtype=float)

for line in inputFile.readlines():

    n, ik, ispin = int(line.split()[0]) - 1,  int(line.split()[1]) - 1, int(line.split()[2])
    E_GGA[n], E_GW[n] = float(line.split()[3]), float(line.split()[4])

    sigma_vxc = E_GW[n] - E_GGA[n]    # this means sigma - vxc
    eqp[n] = np.complex(E_GGA[n] + sigma_vxc)

inputFile.close()

H_G0W0 = np.diag(eqp)   # creates a diagonal matrix out of eqp

inputFile = open('n94'+energy+'.dat', 'r')

counter = 0

for line in inputFile.readlines():
	counter = counter + 1

i = 0

inputFile.seek(0)

offdiag = np.zeros((diagonal_n,diagonal_n), dtype=np.complex)

while (i < counter):
	
	line = inputFile.readline().split()
	n = int(line[0]) - 1
	m = int(line[1]) - 1
        real_bare = float(line[4])
	real_sig = float(line[7])
        real_vxc = float(line[8])
	line = inputFile.readline().split() # read the next line
        imag_bare = float(line[4])
	imag_sig = float(line[7])
	imag_vxc = float(line[8])
	z = np.complex(real_sig - real_vxc,imag_sig - imag_vxc)
        if (n != m): 
            offdiag[n][m] = z # make sure you are only including the offdiags so you don't double count
            offdiag[m][n] = np.conjugate(z)
	i = i + 2 
	
H = H_G0W0 + offdiag

outputFile = open('Sigma'+energy+'.mat','w')

for i in range(np.shape(H)[0]):
    for j in range(np.shape(H)[1]):
        outputFile.write(str(H[i][j]) + ' ')

    outputFile.write('\n')

outputFile.close()

inputFileSigma2eV = open('Sigma2eV.mat', 'r')
inputFileSigma3eV = open('Sigma3eV.mat', 'r')

outputFileM = open('SigmaM.mat', 'w')
outputFileB = open('SigmaB.mat', 'w')

for i in range(np.shape(H)[0]):
    e2eVline = inputFileSigma2eV.readline().split()
    e3eVline = inputFileSigma3eV.readline().split()
    for j in range(np.shape(H)[1]):
        X1 = -2 
        Y1 = np.complex(e2eVline[j])
        X0 = -3
        Y0 = np.complex(e3eVline[j])
        slope = (Y1 - Y0)/(X1 - X0)
        intercept = Y0 - slope*X0
        outputFileM.write(str(slope) + ' ')
        outputFileB.write(str(intercept) + ' ')

    outputFileM.write('\n')
    outputFileB.write('\n')
        
