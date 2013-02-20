#!/usr/bin/python

import sys
import numpy as np
import scipy
import scipy.linalg
import random
from numpy import linalg as LA

e_mol = -2. 

#print len(sys.argv)

if len(sys.argv) == 3:

   sigma_mol = float(sys.argv[1]) 
   gamma = float(sys.argv[2])
   constant_coupling = True

elif len(sys.argv) == 4:

   sigma_mol = float(sys.argv[1])
   gamma = float(sys.argv[2])
   constant_coupling = False
   I = float(sys.argv[3])
   print 'Warning, this was bad way to introduce none constant coupling'
else:
   print 'Usage ',sys.argv[0],' Sigma_mol gamma [coupling strength, for use with Lorenztian]' 
   sys.exit()

print 'sigma_mol: ', sigma_mol
print 'gamma: ', gamma
if constant_coupling == False: print 'I: ', I

print 'adding ',e_mol,' and ',sigma_mol,' gives ',e_mol + sigma_mol

inputFile = open('X_layers_unrelaxed/pulse.dat','r')

inputFile.readline() #
inputFile.readline() # header

spectrum = []
spectrum.append(e_mol)

for line in inputFile.readlines():

    spectrum.append(float(line.split()[0]))

HDFT = np.diag(spectrum)

for i in range(np.shape(HDFT)[0]-1):

   x = spectrum[i+1]
   x0 = spectrum[0]    # DFT peak position
   if constant_coupling == True: coupling = gamma
   else: coupling = I/(1 + ((x - x0)/gamma)**2.)
   HDFT[0][i+1] = coupling
   HDFT[i+1][0] = coupling

#print HDFT

old_eigenvalues, old_eigenvectors = LA.eig(HDFT)

correction = np.zeros((np.shape(HDFT)[0],np.shape(HDFT)[0]), dtype = float)
correction[0][0] = sigma_mol

HGW = HDFT + correction

new_eigenvalues, new_eigenvectors = LA.eig(HGW)

outputFile_eig = open('eig.dat','w')

outputFile_eig.write('# nkptgw: 1 neig: '+ str(len(spectrum)) + '\n')
outputFile_eig.write('# E(DFT) E(Sigma) \n')

outputFile_csv = open('eigenvectors_new.csv','w')

for i in range(len(new_eigenvalues)):
    outputFile_eig.write(str(old_eigenvalues[i]) + ' ' + str(new_eigenvalues[i]) + ' \n')
    outputFile_csv.write(str(new_eigenvalues[i]) + ',')
outputFile_csv.write('\n')

outputFile_wtk = open('gw_wtk.dat','w')

for j in range(len(new_eigenvectors[0])):   # 0 is the index of the molecule State
    alpha_squared = new_eigenvectors[0][j]*new_eigenvectors[0][j]
    outputFile_wtk.write(str(alpha_squared) + '\n')

outputFile_wtk.close()

outputFile_wtk = open('dft_wtk.dat','w')

for j in range(len(old_eigenvectors[0])):   # 0 is the index of the molecule State
    alpha_squared = old_eigenvectors[0][j]*old_eigenvectors[0][j]
    outputFile_wtk.write(str(alpha_squared) + '\n')

outputFile_wtk.close()

for i in range(len(new_eigenvalues)):
    for j in range(len(new_eigenvectors[i])):

        outputFile_csv.write(str(new_eigenvectors[i][j]) + ',')

    outputFile_csv.write('\n')

outputFile_eig.close()
outputFile_csv.close()
outputFile_wtk.close()


