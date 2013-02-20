#!/usr/bin/python

diagonal_n = 3 

import numpy as np
import scipy
import random
from numpy import linalg as LA

e_mol = 1. 
em1 = 2.
em2 = 3.
V = 1.
sigma_mol = -2.8
sigma_metal1 = 0.
sigma_metal2 = 5.


H0 =   np.matrix([[ e_mol, V,   V],
                 [   V,  em1,  0.],
                 [   V,  0., em2]])

eigenvalues, eigenvectors = LA.eig(H0)

diagonalized_DFT = np.diag(eigenvalues)

v1, v2, v3 = eigenvectors[0], eigenvectors[1], eigenvectors[2]

#print eigenvectors

molecular_contrib = np.multiply(sigma_mol, np.matrix([[ v1[0]*v1[0], v1[0]*v2[0], v1[0]*v3[0] ],
                                        [ v2[0]*v1[0], v2[0]*v2[0], v2[0]*v3[0] ],
                                        [ v3[0]*v1[0], v3[0]*v2[0], v3[0]*v3[0] ] ]))

metal1_contrib = sigma_metal1*np.matrix([[ v1[1]*v1[1], v1[1]*v2[1], v1[1]*v3[1] ],
                                        [ v2[1]*v1[1], v2[1]*v2[1], v2[1]*v3[1] ],
                                        [ v3[1]*v1[1], v3[1]*v2[1], v3[1]*v3[1] ] ])

metal2_contrib = sigma_metal2*np.matrix([[ v1[2]*v1[2], v1[2]*v2[2], v1[2]*v3[2] ],
                                        [ v2[2]*v1[2], v2[2]*v2[2], v2[2]*v3[2] ],
                                        [ v3[2]*v1[2], v3[2]*v2[2], v3[2]*v3[2] ] ])


sigma_matrix_with_offdiagonals = molecular_contrib + metal1_contrib + metal2_contrib 

H_GW_full = diagonalized_DFT + sigma_matrix_with_offdiagonals

H_GW_nfull = diagonalized_DFT + np.diag([sigma_matrix_with_offdiagonals[0][0], sigma_matrix_with_offdiagonals[1][1],sigma_matrix_with_offdiagonals[2][2]])

diagonalized_GW_full = np.diag(LA.eigvals(H_GW_full))
diagonalized_GW_nfull = np.diag(LA.eigvals(H_GW_nfull))

print 'original matrix: '
print H0
print
print 'diagonalized matrix'
print diagonalized_DFT 
print
print 'self energies (molecule, metal1, metal2)'
print sigma_mol, sigma_metal1, sigma_metal2

print 'sigma_matrix'
print sigma_matrix_with_offdiagonals
print
print 'H_GW + sigma_matrix'
print H_GW_full
print
print 'diagonalized GW'
#print diagonalized_GW_full
print np.sort([diagonalized_GW_full[0][0], diagonalized_GW_full[1][1],diagonalized_GW_full[2][2]     ])

print 'What happens if I simply add sigma to the DFT H, prior to diagonalization, THEN diagonalize???'

H0[0][0] += sigma_mol
H0[1][1] += sigma_metal1
H0[2][2] += sigma_metal2

dft_plus_sigma = np.diag(LA.eigvals(H0))
#print dft_plus_sigma
print np.sort([dft_plus_sigma[0][0], dft_plus_sigma[1][1],dft_plus_sigma[2][2]])

print 'What about if I didn\'t include offdiagonal elements in my expression for sigma?'

#print diagonalized_GW_nfull
print np.sort([diagonalized_GW_nfull[0][0], diagonalized_GW_nfull[1][1],diagonalized_GW_nfull[2][2]])
