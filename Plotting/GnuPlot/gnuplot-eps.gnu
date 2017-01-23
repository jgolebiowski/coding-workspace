#A generic gnuplot script
set terminal postscript eps enhanced color font 'Helvetica,20' linewidth 2
set output 'test.eps'
set xlabel '{/Symbol Q}_{jol}'
set ylabel 'X^{-2}'
plot sin(x)
