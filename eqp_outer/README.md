This directory contains scripts for renormalizing the output of GW levels so that they are evaluated at the QP energy.

The example.tar file contains a sample calculation where this script can be run. Note that it uses the KIB code to get a gas phase DFT value for the wavefunction in question.

Importantly, the elda values in eqp_outer need to match the values stored in WFN_inner. I do a cheap calc on WFN innner first to get these values
