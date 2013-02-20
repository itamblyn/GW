#!/usr/bin/python

order_of_noise = 0.1

import numpy as np
import scipy
import random
from numpy import linalg as LA


inputFile = open('eig.dat','r')

inputFile.readline() #
inputFile.readline() # skip header

eigenvalues = []

for line in inputFile.readlines():

    eigenvalues.append(np.complex(line.split()[1]))

eigenvalues = np.sort(eigenvalues)

H_G0W0 = np.diag(eigenvalues)

noise_real =                np.random.rand(len(eigenvalues),len(eigenvalues))
noise_imag = scipy.sqrt(-1)*np.random.rand(len(eigenvalues),len(eigenvalues)) 

noise = noise_real + noise_imag

noise *= order_of_noise

H = H_G0W0 + noise

# this is now the unsymmeterized matrix nxm

#print H

for n in range(len(eigenvalues)):

    for m in np.arange(n,len(eigenvalues)):

        H[m][n] = H[n][m].conjugate()

# the matrix is now symmetric

#print H

# what about the fact that the eigenvalues are complex???

new_eigenvalues, new_eigenvectors = LA.eigh(H)

new_eigenvalues = np.sort(new_eigenvalues)

for i in range(len(new_eigenvalues)):

    print str(eigenvalues[i]), str(new_eigenvalues[i]), str((eigenvalues[i] - new_eigenvalues[i]))

#a = np.array([[1+1j, -2j], [2j, 5]])
#print a
#w, v = LA.eigh(a)
#print w, v


#print np.dot(a, v[:, 0]) - w[0] * v[:, 0] # verify 1st e-val/vec pair
#print np.dot(a, v[:, 1]) - w[1] * v[:, 1] # verify 2nd e-val/vec pair
