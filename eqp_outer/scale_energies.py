#!/usr/bin/env python

'''
This is a rough script which reads the output from a GW run based on 
eqp_outer.dat

I have been using this file to evaluate the molecular sub block
'''

inputFile = open('sigma_hp.log','r')
#efermi =  7.364815156
efermi = float(input('What is the DFT Fermi level? ')) 

for i in range(16):
    inputFile.readline()

for i in range(2):

    line = inputFile.readline() # read the line
    n      =int(line.split()[0])
    elda   =float(line.split()[1])
    ecor   =float(line.split()[2])
    x      =float(line.split()[3])
    sxx    =float(line.split()[4])
    ch     =float(line.split()[5])
    sigE   =float(line.split()[6])
    vxc    =float(line.split()[7])
    eqp0   =float(line.split()[8])
    eqp1   =float(line.split()[9])
    chSR   =float(line.split()[10])
    sigSR  =float(line.split()[11])
    eqp0SR =float(line.split()[12])
    eqp1SR =float(line.split()[13])
    Znk    =float(line.split()[14])

    elda_true = float(input('Value of elda from KIB (don\'t subtract Efermi): '))

#    eqp0 = elda - vxc + sig(ecor)


#    eqp1 = eqp0 + (dsig/de) / (1 - dsig/de) * (eqp0 - ecor)

    factor = (eqp1 - eqp0)/(eqp0 - ecor)  
    factorSR = (eqp1SR - eqp0SR)/(eqp0SR - ecor)

    eqp0SR_true = eqp0SR - elda + elda_true
    eqp1SR_true = eqp0SR_true + factorSR * (eqp0SR_true - ecor)
    print 'band=',n, 'eqp1\'=', eqp1SR_true, 'eqp1\'=', eqp1SR_true - efermi, ' eV relative to Ef', round(eqp1SR_true,0), ' is the ecor rec'

'''
    n = band index
 elda = energy eigenvalue
 ecor = corrected energy eigenvalue
    x = bare exchange
   sx = screened exchange at energy ecor
   ch = coulomb hole at energy ecor
  sig = sx + ch = self-energy at energy ecor
  vxc = exchange-correlation potential
 eqp0 = elda - vxc + sig(ecor)
 eqp1 = eqp0 + (dsig/de) / (1 - dsig/de) * (eqp0 - ecor)
  Znk = quasiparticle renormalization factor

        finite_difference_form from sigma.inp file:
        none     = -2 : dsig/de = 0 [skip the expansion]
        backward = -1 : dsig/de = (sig(ecor) - sig(ecor-de)) / de
        central  =  0 : dsig/de = (sig(ecor+de) - sig(ecor-de)) / (2*de)
        forward  =  1 : dsig/de = (sig(ecor+de) - sig(ecor)) / de
        default  =  2 : forward for diagonal and none for off-diagonal
        de is finite_difference_spacing from sigma.inp file
        elda,ecor,x,sx,ch,sig,vxc,eqp0,eqp,de are in eV
        elda and vxc both contain vxc0 so it cancels out
        eqp1 and eqp0 are Eqs. (36-37) from Hybertsen & Louie PRB 34 5390

'''

