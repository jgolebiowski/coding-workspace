#!/bin/bash
temp_list=$(ls | grep '.dat')
list=( $temp_list )
for i in {0..4}
do
temp=${list[$i]}
list[$i]=${temp::-4}

t_line=$(grep '2.11276' $temp)
a_line=($t_line)
value[$i]=${a_line[4]}
#echo ${value[$i]}
done

mydir=$(pwd)
rm -f "$mydir/GNU-script.gnu"
cat > "$mydir/GNU-script.gnu" << EOF
#-----------------------------------------------------------------------
#	THIS IS A GNUPLOT SCRIPT 
#-----------------------------------------------------------------------
set terminal postscript eps enhanced color font 'Helvetica,20' linewidth 2
set output 'energy_landscape.eps'


set xlabel "Distance between two atoms anchoring the functional group [A]"
set ylabel "Energy change [eV]"
set autoscale


plot '${list[0]}.dat' u 3:(\$5-${value[0]}) w lp title '${list[0]}' , \
	'${list[1]}.dat' u 3:(\$5-${value[1]}) w lp title '${list[1]}' , \
        '${list[2]}.dat' u 3:(\$5-${value[2]}) w lp title '${list[2]}' , \
        '${list[3]}.dat' u 3:(\$5-${value[3]}) w lp title '${list[3]}' , \
        '${list[4]}.dat' u 3:(\$5-${value[4]}) w lp title '${list[4]}'
EOF

