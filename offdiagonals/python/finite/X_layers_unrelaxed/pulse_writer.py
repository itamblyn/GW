#!/usr/bin/python

import numpy

stepsize = 0.1
minvalue =  -10.
maxvalue =    0.

outputFile = open('pulse.dat','w')

counter = 0

for i in numpy.arange(minvalue,maxvalue,stepsize):
    counter +=1

outputFile.write('# nkptgw: 1 neig: ' + str(counter) + '\n')
outputFile.write('# E(DFT) pulse\n')

for i in numpy.arange(minvalue,maxvalue,stepsize):
    outputFile.write(str(i) + ' 1.0\n')

outputFile.close()
