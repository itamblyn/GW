#!/bin/tcsh

set sigma=$1
set coupling_width=$2
set coupling_strength=$3

./finite.py $sigma $coupling_width $coupling_strength

echo "eig.dat" > dos_wkpt.in
echo "dft_wtk.dat" >> dos_wkpt.in
./dos_wkpt.x < dos_wkpt.in > /dev/null
rm gw_dos.dat
mv dft_dos.dat dft.dat

echo "eig.dat" > dos_wkpt.in
echo "gw_wtk.dat" >> dos_wkpt.in
./dos_wkpt.x < dos_wkpt.in > /dev/null
rm dft_dos.dat
mv gw_dos.dat gw.dat


set cmd="gnuplot.scr"
cat > $cmd << END
set style data linespoints
set yrange [0:1]
set arrow from ("$sigma" + -2.),0 to ("$sigma" + -2.),0.05 nohead
set arrow from -2.,0 to -2.,0.05 nohead
plot 'dft.dat' t 'no correction applied', 'gw.dat' lt 3 t 'correction applied'
pause -1 "Showing pDOS.\nPress enter to quit"
quit
END

grep -v "\#" eig.dat > eig.tmp
echo -n "DFT position: " 
paste dft_wtk.dat eig.tmp | awk '{sum+=$1*$2; print sum}' | tail -1

grep -v "\#" eig.dat > eig.tmp
echo -n "GW position: "
paste gw_wtk.dat eig.tmp | awk '{sum+=$1*$3; print sum}' | tail -1

rm eig.tmp

gnuplot $cmd

\rm $cmd
