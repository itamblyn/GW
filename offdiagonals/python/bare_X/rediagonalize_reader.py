#!/usr/bin/python

clean = False

HOMO_index = 94 - 1 # band index starts from 1 for BerkeleyGW

diagonal_n = 144

import numpy as np
import scipy
import random
import pylab
from numpy import linalg as LA


inputFile = open('eigX.dat','r')

print 'warning: check if there is a header!!!'

inputFile.readline() #
inputFile.readline() # skip header

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

inputFile = open('offdiag.txt', 'r')

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
	z = np.complex(real_bare - real_vxc,imag_bare - imag_vxc)
        if (n != m): 
            offdiag[n][m] = z # make sure you are only including the offdiags so you don't double count
            offdiag[m][n] = np.conjugate(z)
	i = i + 2 
	
H = H_G0W0 + offdiag

old_eigenvalues, old_eigenvectors = LA.eig(H_G0W0)
new_eigenvalues, new_eigenvectors = LA.eig(H)

for old_index in range(len(new_eigenvalues)):
    new_index = np.argmax(new_eigenvectors[old_index])
    print old_index, np.real(old_eigenvalues[old_index]), np.real(new_eigenvalues[new_index])

#real_GGA = np.real(E_GGA)
#real_GW =  np.real(E_GW)
#real_sGW = np.real(new_eigenvalues)
#outarray  = real_sGW
#outputFile = open('result.csv','w')
#for i in range(len(new_eigenvalues)):
#    outputFile.write( str(i + 1) + ', ' + str(real_GGA[i]) + ', ' + str(real_GW[i]) + ', ' + str(outarray[i]) + '\n')
#outputFile.close()

outputFile = open('eigenvectors_new.csv','w')


for i in range(len(new_eigenvalues)):

    for j in range(len(new_eigenvectors[i])):

        outputFile.write(str(new_eigenvectors[i][j]) + ',')

    outputFile.write('\n')


outputFile.close()
