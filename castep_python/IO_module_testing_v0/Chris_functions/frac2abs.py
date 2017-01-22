#!/usr/bin/python

import sys
import numpy as np

# Script for converting .cell files with fractional atomic positions to absolute atomic positions

filename = str(sys.argv[1])  # First argument is .cell file
pos_digit = 16               # Number of decimal places in atom posns

# Open files and get indicies of important lines
f = open(filename,'r')                         # Open cell file 
cell  = f.readlines()                          # Read file as a list of lines
cell_new = cell
f.seek(0,0)
for num, line in enumerate(f):                 # Find start and end of atom positions section
    if '%BLOCK POSITIONS_FRAC' in line:
        l_1 = num
f.seek(0,0)
cell_new[l_1] = '%BLOCK POSITIONS_ABS\n'
for num, line in enumerate(f):
    if '%ENDBLOCK POSITIONS_FRAC' in line:
        l_2 = num
f.seek(0,0) 
cell_new[l_2] = '%ENDBLOCK POSITIONS_ABS\n'
n = l_2 - l_1                                   # number of atoms 
string = "{0:." + str(pos_digit) + "f}"
for num, line in enumerate(f):                  # Find the start of the lattice vectors (assumed to be BEFORE atom positions)
    if '%BLOCK LATTICE_CART' in line:           # and thus print the new lattice vectors
        l_lat = num
f.close()

# Matrix to convert frac to abs coordinates:    latvec = [[ax,bx,cx],[ay,by,cy],[az,bz,cz]]
latvec=[[float(cell[l_lat+1].split()[0]),float(cell[l_lat+2].split()[0]),float(cell[l_lat+3].split()[0])],[float(cell[l_lat+1].split()[1]),float(cell[l_lat+2].split()[1]),float(cell[l_lat+3].split()[1])],[float(cell[l_lat+1].split()[2]),float(cell[l_lat+2].split()[2]),float(cell[l_lat+3].split()[2])]]

# Cycle through each old atom and assign new coordinates
i = 1
while i < n:
    atom  = str(cell[l_1 + i].split()[0])
    pos_x = float(cell[l_1 + i].split()[1])                 # Old fractional positions
    pos_y = float(cell[l_1 + i].split()[2])
    pos_z = float(cell[l_1 + i].split()[3])
    fracvec = [[pos_x],[pos_y],[pos_z]]                     # Vector of old fractional positions
    absvec = np.dot(latvec,fracvec)                         # Vector of old absolute positions
    newpos_x = float(absvec[0][0])                          # New absolute positions
    newpos_y = float(absvec[1][0])
    newpos_z = float(absvec[2][0])
    cell_new[l_1 + i] = atom + '\t' + str(string.format(newpos_x)) + '\t' + str(string.format(newpos_y)) + '\t' + str(string.format(newpos_z)) + '\n'
    i = i + 1

# Rewrite .cell file with new atom positions
g = open(filename,'w')
g.writelines( cell_new )
g.close

print filename + " updated with all absolute atom positions"
