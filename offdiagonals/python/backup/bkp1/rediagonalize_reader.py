#!/usr/bin/python

#order_of_noise = 0.1

# now we can selectively delete things on the offdiagonal

clean = False

HOMO_index = 94 - 1 # band index starts from 1 for BerkeleyGW

diagonal_n = 160 

import numpy as np
import scipy
import random
from numpy import linalg as LA


inputFile = open('eig.dat','r')

inputFile.readline() #
inputFile.readline() # skip header

eqp = []

E_GW = []
E_GGA = []

for line in inputFile.readlines():

    E_GGA.append(float(line.split()[0]))
    E_GW.append(float(line.split()[1]))

    sigma_vxc = E_GW[-1] - E_GGA[-1]    # this means sigma - vxc

    eqp.append(np.complex(E_GGA[-1] + sigma_vxc))

inputFile.close()

H_G0W0 = np.diag(eqp)   # creates a diagonal matrix out of eqp

#print H_G0W0

#noise_real =                np.random.rand(len(eigenvalues),len(eigenvalues))
#noise_imag = scipy.sqrt(-1)*np.random.rand(len(eigenvalues),len(eigenvalues)) 
#noise = noise_real + noise_imag
#noise *= order_of_noise
#H = H_G0W0 + noise

inputFile = open('offdi.txt', 'r')

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
	real_sig = float(line[7])
        real_vxc = float(line[8])
	line = inputFile.readline().split() # read the next line
	imag_sig = float(line[7])
	imag_vxc = float(line[8])
	z = np.complex(real_sig - real_vxc,imag_sig - imag_vxc)
        if (n != m): offdiag[n][m] = z # make sure you are only including the offdiags so you don't double count
	i = i + 2 
	
H = H_G0W0 + offdiag

#print 'this is now the unsymmeterized matrix'

for n in range(diagonal_n):

    for m in np.arange(n,diagonal_n):

        H[m][n] = H[n][m].conjugate()

# the matrix is now self-adjoint, i.e. Hermitian

#####
#
# ascii art of matrix
#
#####

outputFile = open('H.matrix.full', 'w')

for i in range(diagonal_n):

    for j in range(diagonal_n):

        if (H[i][j] == 0.): outputFile.write('. ')
        else: outputFile.write('X ')

    outputFile.write('\n')

outputFile.close()



if (clean == True):

    for n in range(diagonal_n):

        for m in range(diagonal_n):

            if (n != m):

                if ( n != HOMO_index and m != HOMO_index): H[n][m] = 0.

#####
#
# ascii art of matrix
#
#####

outputFile = open('H.matrix.clean', 'w')

for i in range(diagonal_n):

    for j in range(diagonal_n):

        if (H[i][j] == 0.): outputFile.write('. ')
        else: outputFile.write('X ')

    outputFile.write('\n')

outputFile.close()


new_eigenvalues, new_eigenvectors = LA.eig(H)

#for i in range(len(new_eigenvalues)):

#    if (i == HOMO_index): print str(eqp[i]), str(new_eigenvalues[i]), ' HOMO'
#    else:                 print str(eqp[i]), str(new_eigenvalues[i])

sorted_old_eigenvalues = np.sort(eqp)
sorted_new_eigenvalues = np.sort(new_eigenvalues)

for i in range(len(sorted_new_eigenvalues)):

    print np.real(sorted_old_eigenvalues[i]), np.real(sorted_new_eigenvalues[i])

wtk_array = []

inputFile = open('wtk_k0.dat','r')

for i in range(diagonal_n):

    line = inputFile.readline()

    wtk_array.append(float(line.split()[1]))

inputFile.close()

wtk_array = np.array(wtk_array)

#print wtk_array

for eigenvector in new_eigenvectors:

    tmp_array = []

    for element in eigenvector:

        tmp_array.append(element*element.conjugate())

#    print np.real(np.dot(wtk_array, tmp_array))

#sum = 0.0

#for coeff in new_eigenvectors[0]:

#    sum += coeff*coeff.conjugate()

#print sum

#for element in new_eigenvectors[0]: print element
