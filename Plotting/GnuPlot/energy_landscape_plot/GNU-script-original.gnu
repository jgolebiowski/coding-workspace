#-----------------------------------------------------------------------
#	THIS IS A GNUPLOT SCRIPT 
#-----------------------------------------------------------------------
set terminal postscript eps enhanced color font 'Helvetica,20' linewidth 2
set output 'energy_landscape.eps'


set xlabel "Distance between two atoms anchoring the functional group [A]"
set ylabel "Energy change [eV]"
set autoscale


plot 'C5H2F2.dat' u 3:($5--17058.53453404) w lp title 'C_5H_2F_2' , 	'C5H4O2.dat' u 3:($5--16647.74720168) w lp title 'C_5H_4O_2' ,         'C5H8.dat' u 3:($5--15832.85044608) w lp title 'C_5H_8' ,         'CH2.dat' u 3:($5--15114.57674995) w lp title 'CH_2', 	'C5H4.dat' u 3:($5--15766.63120826) w lp title 'C_5H_4' lt rgb "#DC143C" ,         'C5H4F4.dat' u 3:($5--18417.33807961) w lp title 'C_5H_4F_4'
