#!/usr/bin/python

import sys
import numpy as np

# Script for converting .cell files with absolute atomic positions to fractional atomic positions
# Note script DOES NOT confine atoms to a single unit cell

filename = str(sys.argv[1])  # First argument is .cell file
pos_digit = 16               # Number of decimal places in atom posns

# Open files and get indicies of important lines
f = open(filename,'r')                         # Open cell file 
cell  = f.readlines()                          # Read file as a list of lines
cell_new = cell
f.seek(0,0)
for num, line in enumerate(f):                 # Find start and end of atom positions section
    if '%BLOCK POSITIONS_ABS' in line:
        l_1 = num
f.seek(0,0)
cell_new[l_1] = '%BLOCK POSITIONS_FRAC\n'
for num, line in enumerate(f):
    if '%ENDBLOCK POSITIONS_ABS' in line:
        l_2 = num
f.seek(0,0) 
cell_new[l_2] = '%ENDBLOCK POSITIONS_FRAC\n'
n = l_2 - l_1                                   # number of atoms 
string = "{0:." + str(pos_digit) + "f}"
for num, line in enumerate(f):                  # Find the start of the lattice vectors (assumed to be BEFORE atom positions)
    if '%BLOCK LATTICE_CART' in line:           # and thus print the new lattice vectors
        l_lat = num
f.close()
# Lattice vectors in form:    avec = [ax,ay,az]  
avec = [float(cell[l_lat+1].split()[0]),float(cell[l_lat+1].split()[1]),float(cell[l_lat+1].split()[2])]
bvec = [float(cell[l_lat+2].split()[0]),float(cell[l_lat+2].split()[1]),float(cell[l_lat+2].split()[2])]
cvec = [float(cell[l_lat+3].split()[0]),float(cell[l_lat+3].split()[1]),float(cell[l_lat+3].split()[2])]
a = np.linalg.norm(avec)                        # Lattice parameters
b = np.linalg.norm(bvec)
c = np.linalg.norm(cvec)

# Cycle through each old atom and assign new coordinates
i = 1
while i < n:
    atom  = str(cell[l_1 + i].split()[0])
    pos_x = float(cell[l_1 + i].split()[1])                 # Old absolute positions
    pos_y = float(cell[l_1 + i].split()[2])
    pos_z = float(cell[l_1 + i].split()[3])
    absvec = [[pos_x],[pos_y],[pos_z]]                      # Vector of old absolute positions
    newpos_x = float(np.dot(avec,absvec)/(a**2))          # Fractional positions
    newpos_y = float(np.dot(bvec,absvec)/(b**2))
    newpos_z = float(np.dot(cvec,absvec)/(c**2))
    cell_new[l_1 + i] = atom + '\t' + str(string.format(newpos_x)) + '\t' + str(string.format(newpos_y)) + '\t' + str(string.format(newpos_z)) + '\n'
    i = i + 1

# Rewrite .cell file with new atom positions
g = open(filename,'w')
g.writelines( cell_new )
g.close

print filename + " updated with all fractional atom positions"
