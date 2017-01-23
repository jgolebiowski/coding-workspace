#A generic gnuplot script
set terminal epslatex standalone
set output 'test.tex'
set xlabel '$C_{lol}$'
plot sin(x)


# In order to proceed an ps image must be created from the tex one 
# 1. Load the gnuplot script 
# 2. latex test.tex
# 3. dvips -o test.ps test.dvi
# Bene
