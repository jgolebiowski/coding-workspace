#!/usr/bin/python

import sys

#################################################################
# Confine fractional coordinates to a 0.0<=x<1.0 range
def confine(x):
    x = float(x)
    if x >= 1.000:
        y = x - int(x)
    elif x < 0.000:
        y = 1.0 - (abs(x) - int(abs(x)))
    else:
        y = x
    return y
#################################################################

# Script for shifting all ion positions in a cell by a fractional cell vector shift with no changes to lattice params

filename = str(sys.argv[1]) # First argument is .cell file
shiftx = float(sys.argv[2]) # Second argument is x component of shift
shifty = float(sys.argv[3]) # Third argument is y component of shift
shiftz = float(sys.argv[4]) # Fourth argument is x component of shift
pos_digit = 16              # Number of decimal places in atom posns

# Open files and get indicies of important lines
f = open(filename,'r')
cell  = f.readlines()
cell_new = cell
f.seek(0,0)
for num, line in enumerate(f):
    if '%BLOCK POSITIONS_FRAC' in line:
        l_1 = num
f.seek(0,0)
for num, line in enumerate(f):
    if '%ENDBLOCK POSITIONS_FRAC' in line:
        l_2 = num
f.close()
n = l_2 - l_1               # number of atoms 
i = 1
string = "{0:." + str(pos_digit) + "f}"

# Cycle through each old atom and assign new coordinates
while i < n:
    atom  = str(cell[l_1 + i].split()[0])
    pos_x = float(cell[l_1 + i].split()[1])
    pos_x = confine(pos_x + shiftx)
    pos_y = float(cell[l_1 + i].split()[2])
    pos_y = confine(pos_y + shifty)
    pos_z = float(cell[l_1 + i].split()[3])
    pos_z = confine(pos_z + shiftz)
    cell_new[l_1 + i] = atom + '\t' + str(string.format(pos_x)) + '\t' + str(string.format(pos_y)) + '\t' + str(string.format(pos_z)) + '\n'
    i = i + 1

# Write cell_new to a new .cell file
g = open(filename,'w')
g.writelines( cell_new )
g.close

print filename + " updated with all fractional atom positions shifted by " + str(shiftx) + " " + str(shifty) + " " + str(shiftz)
