#! /usr/bin/env python

import numpy, matplotlib, pylab, sys

#print 'vmin/max are hard coded'
#print 'things should probably be shifted by 1 element (fortran vs python)'

dim = 70 # one more than b_max 

#vmin_value = 0
#vmax_value = 4

if len(sys.argv) == 1:
     print 'usage: ' + sys.argv[0] + ' offdia.txt image.png'

inputFile = open (sys.argv[1],'r')

type_dict = {'real': 0, 'imag': 1}
value_dict = {'x':0, 'sx_x':1, 'ch':2, 'sig':3, 'vxc':4}

OD_array = numpy.ones((dim, dim, 5, 2), dtype=float) # x, sx_x, ch, sig, vxc
OD_array *= -100


for line in inputFile.readlines():
    line_array = line.split()  
    n    = int(line_array[0]) - 1 # convert to python
    m    = int(line_array[1]) - 1 # convert to python
    l    = int(line_array[2]) - 1 # convert to python
    type = line_array[3] # real or imaginary
    x    = float(line_array[4])
    sx_x = float(line_array[5])
    ch   = float(line_array[6])
    sig  = float(line_array[7])
    vxc  = float(line_array[8])

    OD_array[n][m][value_dict['x']][type_dict[type]]    = x
    OD_array[n][m][value_dict['sx_x']][type_dict[type]] = sx_x
    OD_array[n][m][value_dict['ch']][type_dict[type]]   = ch
    OD_array[n][m][value_dict['sig']][type_dict[type]]  = sig
    OD_array[n][m][value_dict['vxc']][type_dict[type]] = vxc

    OD_array[m][n][value_dict['x']][type_dict[type]]    = x
    OD_array[m][n][value_dict['sx_x']][type_dict[type]] = sx_x
    OD_array[m][n][value_dict['ch']][type_dict[type]]   = ch
    OD_array[m][n][value_dict['sig']][type_dict[type]]  = sig
    OD_array[m][n][value_dict['vxc']][type_dict[type]] = vxc

inputFile.close()

#pylab.figure(num=1,figsize=(3,3),facecolor='w',edgecolor='k')

real_COLOR_array = numpy.zeros((dim,dim), dtype = float)
imag_COLOR_array = numpy.zeros((dim,dim), dtype = float)

for i in range(dim):

    for j in range(dim):

        sig = OD_array[i][j][value_dict['sig']][type_dict['real']]
        vxc = OD_array[i][j][value_dict['vxc']][type_dict['real']]
        if ( sig != -100 and i != j):
            real_COLOR_array[i][j] = numpy.abs(sig - vxc)
            real_COLOR_array[i][j] = numpy.abs(sig - vxc)
        else: 
            real_COLOR_array[i][j] = -1.

outputFile = open('offdiag.crix','w')

for i in range(dim):

    for j in range(dim):

        outputFile.write(str(real_COLOR_array[i][j]) + ' ')

    outputFile.write('\n')

outputFile.close()

im = pylab.imshow(real_COLOR_array,vmin=0.0, vmax=0.2)
im.set_interpolation('nearest')
pylab.xticks([1],' ')
pylab.yticks([1],' ')
#pylab.colorbar(cax=pylab.axes([0.85,0.1,0.05,0.8]))
pylab.colorbar()
savefile = sys.argv[2]
pylab.savefig(savefile)
#pylab.show()

#pylab.pcolor(real_COLOR_array)#,vmin=vmin_value,vmax=vmax_value)
#pylab.xticks([0,5,10,15,20],["0","5","10","15","20"])
#pylab.yticks([0,5,10,15,20],["0","5","10","15","20"])
#pylab.colorbar()
#pylab.savefig(savefile)
#pylab.show()
